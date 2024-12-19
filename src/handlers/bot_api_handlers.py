import json
from src.queries.bot_api_queries import (
    create_new_bot_order,
    create_new_transaction,
)

from src.operations.bot_init_ops import BotOrderOps
from src.utils.enums import ORDER_STATUS


def create_new_bot_order_handler(event, _):
    bot_name = event["bot_name"]
    bot_external_id = event["bot_external_id"]
    order_external_id = event["order_external_id"]
    order_by = event["order_by"]
    create_status = create_new_bot_order(
        bot_name=bot_name,
        bot_external_id=bot_external_id,
        order_external_id=order_external_id,
        order_by=order_by,
        order_status=ORDER_STATUS.NEW.name,
    )
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(create_status),
    }


def create_new_bot_transaction_handler(event, _):
    stripe_id = event["stripe_id"]
    stripe_details = event["stripe_details"]
    user_id = event["user_id"]
    bot_id = event["bot_id"]
    create_status = create_new_transaction(
        stripe_id=stripe_id,
        stripe_details=stripe_details,
        user_id=user_id,
        bot_id=bot_id,
        transaction_status=ORDER_STATUS.NEW.name,
    )
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(create_status),
    }


def initialize_order(event, _):
    order_external_id = event["order_external_id"]
    user_id = event["user_id"]
    bot_id = event["bot_id"]
    order_response = BotOrderOps(bot_id=bot_id, user_id=user_id).order_received(
        order_id=order_external_id
    )
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(order_response),
    }


def complete_order(event, _):
    order_external_id = event["order_external_id"]
    user_id = event["user_id"]
    bot_id = event["bot_id"]
    order_response = BotOrderOps(bot_id=bot_id, user_id=user_id).order_completed(
        order_id=order_external_id
    )
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(order_response),
    }
