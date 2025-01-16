import json
import logging
from src.queries.bot_api_queries import (
    create_new_bot_order,
    create_new_transaction,
)
from src.operations.bot_init_ops import BotOrderOps
from src.utils.enums import ORDER_STATUS

# Initialize Logger
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def create_new_bot_order_handler(event, _):
    """
    Handles the creation of a new bot order.

    Parameters:
        event (dict): Contains order details (bot_name, bot_external_id, receipt_id, order_external_id, order_status, order_by).

    Returns:
        dict: HTTP response with order creation status.
    """
    try:
        bot_name = event["bot_name"]
        bot_external_id = event["bot_external_id"]
        receipt_id = event["receipt_id"]
        order_external_id = event["order_external_id"]
        order_status = event["order_status"]
        order_by = event["order_by"]

        logger.info(
            "Processing new bot order: bot_name=%s, bot_external_id=%s, order_external_id=%s, order_status=%s, order_by=%s, receipt_id=%s",
            bot_name,
            bot_external_id,
            order_external_id,
            order_status,
            order_by,
            receipt_id,
        )

        create_status = create_new_bot_order(
            bot_name=bot_name,
            bot_external_id=bot_external_id,
            order_external_id=order_external_id,
            receipt_id=receipt_id,
            order_by=order_by,
            order_status=ORDER_STATUS.INITIALIZED.name,
        )

        logger.info("Order creation status: %s", create_status)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(create_status),
        }

    except KeyError as e:
        logger.error("Missing required key in event: %s", e)
        return {"statusCode": 400, "body": json.dumps({"error": f"Missing key: {e}"})}

    except Exception as e:
        logger.error("Error creating bot order: %s", e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


def create_new_bot_transaction_handler(event, _):
    """
    Handles the creation of a new bot transaction.

    Parameters:
        event (dict): Contains transaction details (payout_id, payout_details, user_id, bot_id).

    Returns:
        dict: HTTP response with transaction creation status.
    """
    try:
        payout_id = event["payout_id"]
        payout_details = event["payout_details"]
        user_id = event["user_id"]
        bot_id = event["bot_id"]

        logger.info(
            "Processing new transaction: payout_id=%s, user_id=%s, bot_id=%s",
            payout_id,
            user_id,
            bot_id,
        )

        create_status = create_new_transaction(
            payout_id=payout_id,
            payout_details=payout_details,
            user_id=user_id,
            bot_id=bot_id,
            transaction_status=ORDER_STATUS.INITIALIZED.name,
        )

        logger.info("Transaction creation status: %s", create_status)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(create_status),
        }

    except KeyError as e:
        logger.error("Missing required key in event: %s", e)
        return {"statusCode": 400, "body": json.dumps({"error": f"Missing key: {e}"})}

    except Exception as e:
        logger.error("Error creating transaction: %s", e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


def initialize_order(event, _):
    """
    Initializes an order and marks it as received.

    Parameters:
        event (dict): Contains order details (order_external_id, user_id, bot_id).

    Returns:
        dict: HTTP response with initialization status.
    """
    try:
        order_external_id = event["order_external_id"]
        user_id = event["user_id"]
        bot_id = event["bot_id"]

        logger.info(
            "Initializing order: order_external_id=%s, user_id=%s, bot_id=%s",
            order_external_id,
            user_id,
            bot_id,
        )

        order_response = BotOrderOps(bot_id=bot_id, user_id=user_id).order_received(
            order_id=order_external_id
        )

        logger.info("Order initialization response: %s", order_response)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(order_response),
        }

    except KeyError as e:
        logger.error("Missing required key in event: %s", e)
        return {"statusCode": 400, "body": json.dumps({"error": f"Missing key: {e}"})}

    except Exception as e:
        logger.error("Error initializing order: %s", e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


def complete_order(event, _):
    """
    Completes an order and updates its status.

    Parameters:
        event (dict): Contains order details (order_external_id, user_id, bot_id).

    Returns:
        dict: HTTP response with completion status.
    """
    try:
        order_external_id = event["order_external_id"]
        user_id = event["user_id"]
        bot_id = event["bot_id"]

        logger.info(
            "Completing order: order_external_id=%s, user_id=%s, bot_id=%s",
            order_external_id,
            user_id,
            bot_id,
        )

        order_response = BotOrderOps(bot_id=bot_id, user_id=user_id).order_completed(
            order_id=order_external_id
        )

        logger.info("Order completion response: %s", order_response)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(order_response),
        }

    except KeyError as e:
        logger.error("Missing required key in event: %s", e)
        return {"statusCode": 400, "body": json.dumps({"error": f"Missing key: {e}"})}

    except Exception as e:
        logger.error("Error completing order: %s", e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
