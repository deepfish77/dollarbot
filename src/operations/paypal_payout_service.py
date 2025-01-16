import requests
import logging
from src.apis.paypal_api import PayPalApiService
from src.queries.paypal_queries import (
    log_paypal_payout,
    log_failed_paypal_payout,
    get_failed_payouts,
    get_failed_payouts_for_user,
)


logger = logging.getLogger(__name__)


class PayPalPayoutService:
    """
    Handles PayPal payouts and retrying failed payouts.
    """

    def __init__(self):
        self.paypal_api = PayPalApiService()

    def create_payout(
        self,
        user_id,
        recipient_email,
        amount,
        currency="USD",
        note="Payout from ServiBots",
    ):
        """
        Create a PayPal payout and store it in the local database.
        """
        url = f"{self.paypal_api.base_url}/v1/payments/payouts"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.paypal_api.access_token}",
        }
        payload = {
            "sender_batch_header": {
                "sender_batch_id": f"batch_{recipient_email}",
                "email_subject": "You have received a payout!",
            },
            "items": [
                {
                    "recipient_type": "EMAIL",
                    "amount": {"value": f"{amount:.2f}", "currency": currency},
                    "receiver": recipient_email,
                    "note": note,
                    "sender_item_id": f"payout_{recipient_email}",
                }
            ],
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()

            payout_id = response.json().get("batch_header", {}).get("payout_batch_id")
            log_paypal_payout(payout_id, user_id, amount, "PENDING")
            logger.info("Successfully created PayPal payout: %s", payout_id)
            return payout_id

        except requests.exceptions.RequestException as e:
            logger.error("PayPal Payout failed: %s", e)
            log_failed_paypal_payout(
                f"batch_{recipient_email}", user_id, amount, str(e)
            )
            return None

    def get_payout_status(self, payout_id):
        """
        Get the status of a PayPal payout.
        """
        url = f"{self.paypal_api.base_url}/v1/payments/payouts/{payout_id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.paypal_api.access_token}",
        }

        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.json()

    def retry_failed_payouts(self):
        """
        Retry all failed PayPal payouts.
        """
        failed_payouts = get_failed_payouts()
        if failed_payouts.empty:
            logger.info("No failed payouts to retry.")
            return

        for _, row in failed_payouts.iterrows():
            try:
                self.create_payout(
                    row["user_id"], row["recipient_email"], row["amount"]
                )
            except Exception as e:
                logger.error(
                    "Retry failed for payout: %s, Error: %s", row["payout_id"], e
                )

    def retry_failed_payouts_for_user(self, user_id):
        """
        Retry all failed PayPal payouts for a specific user.
        """
        failed_payouts = get_failed_payouts_for_user(user_id)
        if failed_payouts is None or failed_payouts.empty:
            logger.info("No failed payouts to retry for user: %s", user_id)
            return {
                "success": False,
                "message": f"No failed payouts found for user {user_id}",
            }

        retried_payouts = []
        failed_retries = []

        for _, row in failed_payouts.iterrows():
            try:
                self.create_payout(row["user_id"], row["payout_id"], row["amount"])
                retried_payouts.append(row["payout_id"])
                logger.info(
                    "Successfully retried payout for user: %s, payout: %s",
                    user_id,
                    row["payout_id"],
                )
            except Exception as e:
                logger.error(
                    "Retry failed for payout: %s, Error: %s", row["payout_id"], e
                )
                failed_retries.append(row["payout_id"])

        return {
            "success": True,
            "retried_payouts": retried_payouts,
            "failed_retries": failed_retries,
        }
