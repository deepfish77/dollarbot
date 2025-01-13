import logging
from wallet_service import WalletService

# Initialize logger
logger = logging.getLogger(__name__)
wallet_service = WalletService()


def check_balance_handler(event, _):
    """Lambda handler to check wallet balance."""
    user_id = event["pathParameters"]["user_id"]
    logger.info("Received request to check balance for user_id: %s", user_id)

    balance = wallet_service.check_balance(user_id)
    response = {
        "statusCode": 200,
        "body": f"User {user_id} has a balance of ${balance:.2f}",
    }
    logger.info(
        "Responding with balance for user_id: %s, balance: %s", user_id, balance
    )
    return response


def deposit_handler(event, _):
    """Lambda handler to deposit funds to the wallet."""
    body = event["body"]
    user_id = body["user_id"]
    amount = int(body["amount"])

    logger.info("Received request to deposit %s to user_id: %s", amount / 100, user_id)

    success = wallet_service.deposit(user_id, amount)
    if success:
        response = {
            "statusCode": 200,
            "body": f"Deposited ${amount / 100:.2f} to user {user_id}'s wallet",
        }
        logger.info("Successfully deposited %s to user_id: %s", amount / 100, user_id)
    else:
        response = {"statusCode": 500, "body": "Failed to deposit funds"}
        logger.error("Failed to deposit %s to user_id: %s", amount / 100, user_id)

    return response


def deduct_handler(event, _):
    """Lambda handler to deduct funds from the wallet."""
    user_id = event["user_id"]
    amount = event["amount"]

    logger.info("Received request to deduct %s from user_id: %s", amount / 100, user_id)

    success = wallet_service.deduct(user_id, amount)
    if success:
        response = {
            "statusCode": 200,
            "body": f"Deducted ${amount / 100:.2f} from user {user_id}'s wallet",
        }
        logger.info("Successfully deducted %s from user_id: %s", amount / 100, user_id)
    else:
        response = {"statusCode": 400, "body": "Insufficient balance"}
        logger.error(
            "Failed to deduct %s from user_id: %s due to insufficient balance",
            amount / 100,
            user_id,
        )

    return response
