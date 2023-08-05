from datetime import datetime
import logging
from typing import List

from aporia.consts import LOGGER_NAME
from aporia.errors import AporiaError
from aporia.graphql_client import GraphQLClient

logger = logging.getLogger(LOGGER_NAME)


REQUIRED_FIELDS = {"id", "features", "prediction"}


async def log_batch_prediction(
    graphql_client: GraphQLClient,
    model_id: str,
    model_version: str,
    environment: str,
    serialized_predictions: List[dict],
    await_insert: bool,
):
    """Reports a batch of predictions.

    Args:
        graphql_client (GraphQLClient): GraphQL client
        model_id (str): Model ID
        model_version (str): Model version
        environment (str): Environment in which aporia is running.
        serialized_predictions (List[dict]): List of serialized prediction dicts.
        await_insert (bool): True if the controller should wait for the predictions
            to be stored before responding to the sdk.
    """
    query = """
        mutation LogPredict(
            $modelId: String!,
            $modelVersion: String!,
            $environment: String!,
            $predictions: [Prediction]!
            $isSync: Boolean!
        ) {
            logPredictions(
                modelId: $modelId,
                modelVersion: $modelVersion,
                environment: $environment,
                predictions: $predictions
                isSync: $isSync
            ) {
                warnings
            }
        }
    """

    variables = {
        "modelId": model_id,
        "modelVersion": model_version,
        "environment": environment,
        "predictions": serialized_predictions,
        "isSync": await_insert,
    }

    result = await graphql_client.query_with_retries(query, variables)
    for warning in result["logPredictions"]["warnings"]:
        logger.warning(warning)


def serialize_prediction_batch(predictions: List[dict]) -> List[dict]:
    """Serializes prediction batches.

    Args:
        predictions (List[dict]): Prediction dicts with user data and timestamp

    Returns:
        List[dict]: Serialized prediction batch.
    """
    prepared_predictions = []  # type: ignore

    for predict in predictions:
        try:
            predict_data = predict["data"]

            missing_fields = REQUIRED_FIELDS - predict_data.keys()
            if len(missing_fields) > 0:
                raise AporiaError("Missing required fields {}".format(missing_fields))

            occurred_at = predict_data.get("occurred_at")
            if occurred_at is None:
                occurred_at = predict["timestamp"]

            prepared_predict = {
                "id": predict_data["id"],
                "features": predict_data["features"],
                "prediction": predict_data["prediction"],
                "occurredAt": occurred_at.isoformat(),
            }

            prepared_predictions.append(prepared_predict)

        except Exception as err:
            logger.error("Failed to serialize prediction, error: {}".format(err))
            continue

    return prepared_predictions


def is_valid_prediction(predict: dict) -> bool:
    """Checks if a prediction is valid.

    This function exists mostly for debugging purposes.

    Args:
        predict (dict): Prediction dict

    Returns:
        bool: True if the prediction is valid.

    Notes:
        * This function is only used in debug mode.
    """
    missing_fields = REQUIRED_FIELDS - predict.keys()
    if len(missing_fields) > 0:
        logger.debug("Invalid prediction, missing required fields {}".format(missing_fields))
        return False

    if not (isinstance(predict["features"], dict) and len(predict["features"]) > 0):
        logger.debug("Invalid input format for features parameter - expected a non-empty dict")
        return False

    if not (isinstance(predict["prediction"], dict) and len(predict["prediction"]) > 0):
        logger.debug("Invalid input format for prediction parameter - expected a non-empty dict")
        return False

    if predict.get("occurred_at") is not None and not isinstance(predict["occurred_at"], datetime):
        logger.debug("Invalid input format for occurred_at parameter - expected datetime")
        return False

    return True
