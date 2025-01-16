import json
import logging
from src.operations.developer_balance_calc import DeveloperBalanceService

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def user_balance_handler(event, _):
    """
    Lambda function to handle requests for user balance, transaction history, and failed transactions.
    """
    try:
        # Parse the request
        user_id = event["user_id"]
        action = event["action"]

        # Initialize the service
        service = DeveloperBalanceService()

        # Handle actions
        if action == "get_balance":
            response = service.get_developer_balance(user_id)
        elif action == "get_transaction_history":
            response = service.get_transaction_history(user_id)
        elif action == "get_failed_transactions":
            response = service.get_failed_transactions(user_id)
        else:
            response = {"success": False, "message": "Invalid action specified."}

        return response

    except Exception as e:
        logger.error("Error processing user balance request: %s", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"success": False, "message": str(e)}),
        }
