import logging
from typing import Optional, Dict
import stripe
from src.queries.stripe_webhook_queries import log_failed_payout

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

class StripeWebhookService:
    """
    A service class to handle Stripe webhooks for payout failures.
    """

    @staticmethod
    def process_stripe_webhook(event):
        """
        Process a Stripe webhook event.

        :param event: The Stripe webhook event.
        :return: A success message or an error message.
        """
        event_type = event.get("type")
        logger.info("Received Stripe webhook event: %s", event_type)

        if event_type == "payout.failed":
            return StripeWebhookService.handle_stripe_payout_failed(event["data"]["object"])
        else:
            logger.warning("Unhandled event type: %s", event_type)
            return {"status": "unhandled", "message": "Event type not handled"}

    @staticmethod
    def handle_stripe_payout_failed(payout):
        """
        Handle the payout.failed event from Stripe.

        :param payout: The payout object from the event.
        :return: A success message or an error message.
        """
        account_id = payout["destination"]
        payout_id = payout["id"]
        failure_reason = payout["failure_message"]

        logger.info("Handling failed payout for payout_id: %s, account_id: %s", payout_id, account_id)

        success = log_failed_payout(account_id, payout_id, failure_reason)
        if success:
            logger.info("Failed payout logged successfully: %s", payout_id)
            return {"status": "success", "message": "Failed payout logged"}
        else:
            logger.error("Failed to log payout failure for payout_id: %s", payout_id)
            return {"status": "error", "message": "Failed to log payout failure"}
 

    @staticmethod
    def create_stripe_payout(amount: int, connected_account_id: str, currency: str = "usd", description: Optional[str] = None) -> Optional[str]:
        """
        Create a payout to a bank account or debit card from a connected account.

        :param amount: Amount to payout in the smallest currency unit (e.g., cents).
        :param connected_account_id: The Stripe connected account ID.
        :param currency: The currency (default is USD).
        :param description: Optional description for the payout.
        :return: The payout ID if successful, None otherwise.
        """
        try:
            logger.info("Creating payout of %d %s to account %s", amount, currency, connected_account_id)
            payout = stripe.Payout.create(
                amount=amount,
                currency=currency,
                destination=connected_account_id,
                description=description,
                stripe_account=connected_account_id
            )
            logger.info("Payout created successfully: %s", payout['id'])
            return payout['id']
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return None

    @staticmethod
    def check_stripe_balance() -> Optional[Dict]:
        """
        Check the balance of the platform account.

        :return: A dictionary containing balance details, or None if an error occurs.
        """
        try:
            logger.info("Checking platform account balance")
            balance = stripe.Balance.retrieve()
            logger.info("Balance retrieved successfully")
            return balance
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return None