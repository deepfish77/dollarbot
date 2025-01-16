from src.operations.paypal_payout_service import PayPalPayoutService
from src.queries.paypal_queries import get_paypal_user_query

payout_service = PayPalPayoutService()


def create_payout_handler(event, _):
    user_id = event["user_id"]
    recipient_email = event["recipient_email"]
    amount = event["amount"]

    payout_id = payout_service.create_payout(user_id, recipient_email, amount)

    return {"payout_id": payout_id}


def get_payout_status_handler(event, _):
    payout_id = event["payout_id"]
    status = payout_service.get_payout_status(payout_id)
    return status


def get_user_payouts_handler(event, _):
    user_id = event["user_id"]
    payouts = get_paypal_user_query(user_id)

    if payouts.empty:
        return {"success": False, "message": "No payouts found for this user."}

    return {"payouts": payouts.to_dict(orient="records")}


def lambda_retry_failed_payouts(event, _):
    payout_service.retry_failed_payouts()
    return {"message": "Retry process completed."}


def lambda_retry_failed_payouts_for_user(event, _):
    """
    Lambda function to retry all failed payouts for a specific user.
    """
    user_id = event.get("user_id")
    if not user_id:
        return {"success": False, "message": "User ID is required"}

    result = payout_service.retry_failed_payouts_for_user(user_id)
    return result
