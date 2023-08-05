from concurrent.futures import ALL_COMPLETED, wait
from datetime import datetime, timezone
import logging
from typing import Any, cast, Dict, Iterable, List, Optional, Union

import aporia
from aporia.api.log_json import log_json
from aporia.api.log_predict import (
    is_valid_prediction,
    log_batch_prediction,
    serialize_prediction_batch,
)
from aporia.config import Config
from aporia.consts import LOGGER_NAME
from aporia.errors import handle_error
from aporia.event_loop import EventLoop
from aporia.graphql_client import GraphQLClient
from aporia.prediction_queue import PredictionQueue


logger = logging.getLogger(LOGGER_NAME)


SupportedValueType = Union[float, int, bool, str]


class BaseModel:
    """Base class for Model objects."""

    def __init__(
        self,
        model_id: str,
        model_version: str,
        graphql_client: Optional[GraphQLClient],
        event_loop: Optional[EventLoop],
        config: Optional[Config],
    ):
        """Initializes a BaseModel object.

        Args:
            model_id (str): Model identifier
            model_version (str): Model version
            graphql_client (Optional[GraphQLClient]): GraphQL client
            event_loop (Optional[EventLoop]): AsyncIO event loop
            config (Optional[Config]): Aporia config
        """
        logger.debug(
            "Initializing model object for model {} version {}".format(model_id, model_version)
        )
        self._model_ready = False

        self.model_id = model_id
        self.model_version = model_version
        self._graphql_client = cast(GraphQLClient, graphql_client)
        self._event_loop = cast(EventLoop, event_loop)
        self._config = cast(Config, config)
        # We keep a list of all tasks that were not awaited, to allow flushing
        # We have to do this manually to support python versions below
        # 3.7 (otherwise we could use asyncio.all_tasks())
        self._futures = []  # type: ignore

        if event_loop is not None and graphql_client is not None and config is not None:
            prediction_queue = self._init_prediction_queue()
            if prediction_queue is not None:
                self._prediction_queue = prediction_queue
                self._model_ready = True

        if not self._model_ready:
            logger.error("Model object initialization failed - model operations will not work.")

    def _init_prediction_queue(self) -> Optional[PredictionQueue]:
        try:
            return PredictionQueue(
                event_loop=self._event_loop,
                batch_size=self._config.prediction_queue_batch_size,
                max_size=self._config.prediction_queue_max_predictions,
                flush_interval=self._config.prediction_queue_flush_interval,
                flush_callback=self._log_batch_prediction,
            )
        except Exception as err:
            handle_error(
                message="Initializing prediction queue failed, error: {}".format(str(err)),
                add_trace=self._config.debug,
                raise_exception=self._config.throw_errors,
                original_exception=err,
                log_level=logging.ERROR,
            )
            return None

    def log_prediction(
        self,
        id: str,
        features: Dict[str, SupportedValueType],
        prediction: Dict[str, SupportedValueType],
        occurred_at: Optional[datetime] = None,
    ):
        """Logs a single prediction.

        Args:
            id (str): Prediction identifier.
            features (Dict[str, SupportedValueType]): Values for all the features in the prediction
            prediction (Dict[str, SupportedValueType]): Prediction result
            occurred_at (datetime, optional): Prediction timestamp. Defaults to None.

        Note:
            * If occurred_at is None, it will be reported as datetime.now()
        """
        self.log_batch_prediction(
            predictions=[
                dict(
                    id=id,
                    features=features,
                    prediction=prediction,
                    occurred_at=occurred_at,
                )
            ]
        )

    def log_batch_prediction(self, predictions: Iterable[dict]):
        """Logs multiple predictions.

        Args:
            predictions (Iterable[dict]): An iterable that produces prediction dicts.
                Each prediction dict MUST contain the following keys:
                    * id (str): Prediction identifier.
                    * features (Dict[str, SupportedValueType]): Values for all the features
                        in the prediction
                    * prediction (Dict[str, SupportedValueType]): Prediction result
                Each prediction dict MAY also contain the following keys:
                    * occurred_at (datetime): Prediction timestamp.

        Notes:
            * If occurred_at is None in any of the predictions, it will be reported as datetime.now()
        """
        if not self._model_ready:
            return

        logger.debug("Logging predictions")
        try:
            if self._config.debug:
                logger.debug("Validating predictions")
                for i, predict in enumerate(predictions):
                    if is_valid_prediction(predict):
                        logger.debug("Prediction {} is valid".format(i))
                    else:
                        logger.debug("Prediction {} is not valid".format(i))

            now = datetime.now(tz=timezone.utc)
            predictions_with_timestamps = [
                {"data": predict, "timestamp": now} for predict in predictions
            ]

            prediction_count = self._event_loop.run_coroutine(
                self._prediction_queue.put(predictions=predictions_with_timestamps)
            )

            dropped_predictions = len(predictions_with_timestamps) - prediction_count
            if dropped_predictions > 0:
                logger.warning(
                    "Reached prediction limit, dropped {} predictions.".format(dropped_predictions)
                )

        except Exception as err:
            handle_error(
                message="Logging prediction batch failed, error: {}".format(str(err)),
                add_trace=self._config.debug,
                raise_exception=False,
                original_exception=err,
                log_level=logging.ERROR,
            )

    async def _log_batch_prediction(self, predictions_with_timestamps: List[dict]):
        try:
            serialized_predictions = serialize_prediction_batch(predictions_with_timestamps)

            if len(serialized_predictions) > 0:
                await log_batch_prediction(
                    graphql_client=self._graphql_client,
                    model_id=self.model_id,
                    model_version=self.model_version,
                    environment=self._config.environment,
                    serialized_predictions=serialized_predictions,
                    await_insert=self._config.debug,
                )
        except Exception as err:
            handle_error(
                message="Logging prediction failed, error: {}".format(str(err)),
                add_trace=self._config.debug,
                raise_exception=False,
                original_exception=err,
                log_level=logging.ERROR,
            )

    def log_json(self, data: Any):
        """Logs arbitrary data.

        Args:
            data (Any): Data to log, must be JSON serializable
        """
        if not self._model_ready:
            return

        logger.debug("Logging arbitrary data.")
        try:
            future = self._event_loop.create_task(self._log_json(data=data))
            self._futures.append(future)
        except Exception as err:
            handle_error(
                message="Logging arbitrary data failed, error: {}".format(str(err)),
                add_trace=self._config.debug,
                raise_exception=False,
                original_exception=err,
                log_level=logging.ERROR,
            )

    async def _log_json(self, data: Any):
        try:
            await log_json(
                graphql_client=self._graphql_client,
                model_id=self.model_id,
                model_version=self.model_version,
                environment=self._config.environment,
                data=data,
            )
        except Exception as err:
            handle_error(
                message="Logging arbitrary data failed, error: {}".format(str(err)),
                add_trace=self._config.debug,
                raise_exception=False,
                original_exception=err,
                log_level=logging.ERROR,
            )

    def flush(self, timeout: Optional[int] = None) -> Optional[int]:
        """Waits for all currently scheduled tasks to finish.

        Args:
            timeout (int, optional): Maximum number of seconds to wait for tasks to
                complete. Default to None (No timeout).

        Returns:
            Optional[int]: Number of tasks that haven't finished running.
        """
        if not self._model_ready:
            return None

        try:
            futures = self._futures
            self._futures = []

            logger.debug("Flusing predictions.")
            # Add a task that flushes the queue, and another that waits for the flush to complete
            futures.append(self._event_loop.create_task(self._prediction_queue.flush()))
            futures.append(self._event_loop.create_task(self._prediction_queue.join()))

            logger.debug("Waiting for {} scheduled tasks to finish executing.".format(len(futures)))
            done, not_done = wait(futures, timeout=timeout, return_when=ALL_COMPLETED)

            logger.debug(
                "{} tasks finished, {} tasks not finished.".format(len(done), len(not_done))
            )
            self._futures.extend(not_done)

            return len(not_done)
        except Exception as err:
            handle_error(
                message="Flushing remaining data failed, error: {}".format(str(err)),
                add_trace=self._config.debug,
                raise_exception=self._config.throw_errors,
                original_exception=err,
                log_level=logging.ERROR,
            )

        return None


class Model(BaseModel):
    """Model object."""

    def __init__(self, model_id: str, model_version: str):
        """Initializes a Model object.

        Args:
            model_id (str): Model identifier, as received from the Aporia dashboard.
            model_version (str): Model version - this can be any string that represents the model
                version, such as "v1" or a git commit hash.
        """
        if aporia.context is None:
            logger.error("Aporia was not initialized.")
            super().__init__(
                model_id=model_id,
                model_version=model_version,
                graphql_client=None,
                event_loop=None,
                config=None,
            )
        else:
            super().__init__(
                model_id=model_id,
                model_version=model_version,
                graphql_client=aporia.context.graphql_client,
                event_loop=aporia.context.event_loop,
                config=aporia.context.config,
            )
