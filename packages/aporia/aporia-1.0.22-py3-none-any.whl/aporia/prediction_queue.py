import asyncio
import logging
from typing import Awaitable, Callable, Iterable, List

from aporia.consts import LOGGER_NAME
from aporia.event_loop import EventLoop


logger = logging.getLogger(LOGGER_NAME)


class PredictionQueue:
    """Queue for prediction batching."""

    def __init__(
        self,
        event_loop: EventLoop,
        batch_size: int,
        max_size: int,
        flush_interval: int,
        flush_callback: Callable[[List[dict]], Awaitable[None]],
    ):
        """Initializes a PredictionQueue.

        Args:
            event_loop (EventLoop): Event loop for async operations
            batch_size (int): Prediction batch size
            max_size (int): Maximum number of predictions in the queue.
            flush_interval (int): Interval for periodic flushes.
            flush_callback (Callable[[List[dict]], Awaitable[None]]): An awaitable function
                to call to flush predictions.
        """
        self.batch_size = batch_size
        self.max_size = max_size
        self.partial_batch = []  # type: ignore
        self.scheduled_batches = 0
        self.flush_callback = flush_callback

        # The queue has to be initialized in the asyncio loop
        self.queue = event_loop.run_coroutine(self._init_queue())
        event_loop.create_task(self._flush_on_interval(flush_interval))

    @staticmethod
    async def _init_queue() -> asyncio.Queue:
        return asyncio.Queue()

    def __len__(self) -> int:
        """Calculates the length of the queue.

        Returns:
            int: Total number of predictions in the queue.
        """
        # Since we want to limit the number of predictions in memory, we have to consider not
        # only the batches that are in the queue, but also the ones that have been scheduled
        # for sending but have not yet been sent.
        return (
            self.scheduled_batches * self.batch_size
            + len(self.partial_batch)
            + self.queue.qsize() * self.batch_size
        )

    async def _flush_on_interval(self, interval: int):
        while True:
            await asyncio.sleep(interval)
            await self.flush()

    async def put(self, predictions: Iterable[dict]) -> int:
        """Inserts predictions to the queue.

        Args:
            predictions (Iterable[dict]): Predictions to insert

        Returns:
            int: Number of predictions added to the queue.

        Notes;
            * Any predictions above the max queue size will be discarded.
        """
        for count, predict in enumerate(predictions, start=1):
            if len(self) >= self.max_size:
                logger.warning(
                    "Maximum number of predictions reached, dropping remaining predictions."
                )
                count -= 1
                break

            if len(self.partial_batch) < self.batch_size:
                self.partial_batch.append(predict)

            if len(self.partial_batch) == self.batch_size:
                # The queue is only accessed from the asyncio loop, and it has no
                # max size, to put_nowait is safe.
                self.queue.put_nowait(self.partial_batch)
                self.partial_batch = []

        if not self.queue.empty():
            asyncio.ensure_future(self.flush())

        return count

    async def flush(self):
        """Flushes the prediction queue."""
        if len(self.partial_batch) > 0:
            self.queue.put_nowait(self.partial_batch)
            self.partial_batch = []

        flush_tasks = []
        # The queue is only accessed from the asyncio loop, meaning only
        # one flush() will run at any given moment, so get_nowait is safe here.
        while not self.queue.empty():
            batch = self.queue.get_nowait()
            flush_tasks.append(self.flush_callback(batch))

        self.scheduled_batches += len(flush_tasks)
        await asyncio.gather(*flush_tasks, return_exceptions=True)

        self.scheduled_batches -= len(flush_tasks)
        for _ in flush_tasks:
            self.queue.task_done()

    async def join(self):
        """Wait for all scheduled predictions to be sent."""
        await self.queue.join()
