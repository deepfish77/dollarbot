import logging
from src.operations.paypal_payment_backup_service import PayPalService
from src.operations.paypal_user_service import PayPalUserService


# Initialize logger
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

# Initialize PayPal service
paypal_service = PayPalService()


def create_paypal_payment_handler(event, _):
    """
    Lambda handler to create a new PayPal payment.
    This is a backup functionality
    """
    body = event["body"]
    user_id = body["user_id"]
    amount = float(body["amount"])

    logger.info(
        "Received request to create PayPal payment for user_id: %s, amount: %.2f",
        user_id,
        amount,
    )

    approval_url = paypal_service.create_transaction(user_id, amount)
    if approval_url:
        return {"statusCode": 200, "body": {"approval_url": approval_url}}
    else:
        return {"statusCode": 500, "body": "Failed to create PayPal payment"}


def update_paypal_transaction_status_handler(event, _):
    """
    Lambda handler to update the status of a PayPal transaction.
    """
    body = event["body"]
    transaction_id = body["transaction_id"]
    status = body["status"]

    logger.info(
        "Received request to update PayPal transaction status for transaction_id: %s to status: %s",
        transaction_id,
        status,
    )

    success = paypal_service.update_paypal_transaction_status(transaction_id, status)
    if success:
        return {
            "statusCode": 200,
            "body": f"Updated PayPal transaction {transaction_id} to status: {status}",
        }
    else:
        return {"statusCode": 500, "body": "Failed to update PayPal transaction status"}


def create_paypal_user_handler(event, _):
    """
    Lambda handler to create a new PayPal user.
    """

    user_id = event["user_id"]
    paypal_email = event["paypal_email"]
    paypal_user_service = PayPalUserService()

    logger.info("Received request to create PayPal user for user_id: %s", user_id)

    success = paypal_user_service.create_user(user_id, paypal_email)
    if success:
        return {
            "statusCode": 200,
            "body": f"Successfully created PayPal user for user {user_id}",
        }
    else:
        return {"statusCode": 500, "body": "Failed to create PayPal user"}
