import logging
from src.operations.paypal_payout_service import PayPalPayoutService
from src.queries.paypal_queries import get_paypal_user_query

# Initialize Logger
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

# Initialize PayPal Payout Service
payout_service = PayPalPayoutService()


def create_payout_handler(event, _):
    """
    Handles PayPal payout creation.

    Parameters:
        event (dict): Contains `user_id`, `recipient_email`, and `amount` for payout.

    Returns:
        dict: Payout ID if successful, or an error message.
    """
    user_id = event.get("user_id")
    recipient_email = event.get("recipient_email")
    amount = event.get("amount")

    if not user_id or not recipient_email or not amount:
        logger.error("Missing required payout parameters.")
        return {"success": False, "message": "Missing required parameters."}

    logger.info(
        "Processing payout for user_id: %s, recipient: %s, amount: %s",
        user_id,
        recipient_email,
        amount,
    )

    payout_id = payout_service.create_payout(user_id, recipient_email, amount)

    if payout_id:
        logger.info("Payout created successfully: %s", payout_id)
        return {"success": True, "payout_id": payout_id}
    else:
        logger.error("Failed to create payout for user_id: %s", user_id)
        return {"success": False, "message": "Payout creation failed."}


def get_payout_status_handler(event, _):
    """
    Retrieves the status of a PayPal payout.

    Parameters:
        event (dict): Contains `payout_id`.

    Returns:
        dict: Payout status details.
    """
    payout_id = event.get("payout_id")

    if not payout_id:
        logger.error("Payout ID is missing from request.")
        return {"success": False, "message": "Payout ID is required."}

    logger.info("Fetching payout status for payout_id: %s", payout_id)

    status = payout_service.get_payout_status(payout_id)

    if status:
        logger.info("Payout status retrieved successfully: %s", status)
        return {"success": True, "status": status}
    else:
        logger.error("Failed to retrieve status for payout_id: %s", payout_id)
        return {"success": False, "message": "Failed to fetch payout status."}


def get_user_payouts_handler(event, _):
    """
    Retrieves all payouts for a given user.

    Parameters:
        event (dict): Contains `user_id`.

    Returns:
        dict: List of payouts if available, or an error message.
    """
    user_id = event.get("user_id")

    if not user_id:
        logger.error("User ID is missing from request.")
        return {"success": False, "message": "User ID is required."}

    logger.info("Fetching payouts for user_id: %s", user_id)

    payouts = get_paypal_user_query(user_id)

    if payouts.empty:
        logger.info("No payouts found for user_id: %s", user_id)
        return {"success": False, "message": "No payouts found for this user."}

    logger.info("Payouts retrieved successfully for user_id: %s", user_id)
    return {"success": True, "payouts": payouts.to_dict(orient="records")}


def lambda_retry_failed_payouts(event, _):
    """
    Retries all failed PayPal payouts.

    Parameters:
        event (dict): Unused.

    Returns:
        dict: Confirmation message.
    """
    logger.info("Retrying all failed PayPal payouts.")

    payout_service.retry_failed_payouts()

    logger.info("Retry process for all failed payouts completed.")
    return {"success": True, "message": "Retry process completed."}


def lambda_retry_failed_payouts_for_user(event, _):
    """
    Retries all failed PayPal payouts for a specific user.

    Parameters:
        event (dict): Contains `user_id`.

    Returns:
        dict: Success message or failure response.
    """
    user_id = event.get("user_id")

    if not user_id:
        logger.error("User ID is missing from request.")
        return {"success": False, "message": "User ID is required."}

    logger.info("Retrying failed payouts for user_id: %s", user_id)

    result = payout_service.retry_failed_payouts_for_user(user_id)

    if result["retried_payouts"]:
        logger.info("Successfully retried payouts for user_id: %s", user_id)
    if result["failed_retries"]:
        logger.warning("Some payouts failed to retry for user_id: %s", user_id)

    return result
