import logging
import stripe
from src.operations.compliance_ops import ComplianceService

logger = logging.getLogger(__name__)

class StripeWebhookService:
    """
    A service to handle Stripe webhooks.
    """

    @staticmethod
    def process_webhook(event):
        """
        Process a Stripe webhook event.
        """
        event_type = event.get("type")
        logger.info("Received Stripe webhook event: %s", event_type)

        if event_type == "account.updated":
            return ComplianceService.handle_account_update(event["data"]["object"])
        elif event_type == "transfer.failed":
            return ComplianceService.handle_transfer_failed(event["data"]["object"])
        else:
            logger.warning("Unhandled event type: %s", event_type)
            return {"status": "unhandled", "message": "Event type not handled"}
