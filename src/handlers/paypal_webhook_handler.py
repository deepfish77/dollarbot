import json
import logging
from src.queries.paypal_queries import update_paypal_payout_status

# Initialize logger
logger = logging.getLogger(__name__)

def paypal_webhook_handler(event, _):
    """
    Handles PayPal Webhook events to update payout status in the database.
    """
    try:
        body = json.loads(event["body"])
        event_type = body.get("event_type")
        payout_item_id = body["resource"]["payout_item_id"]
        transaction_status = body["resource"]["transaction_status"]

        logger.info("Received PayPal webhook event: %s", event_type)

        # Map PayPal status to local DB status
        status_mapping = {
            "SUCCESS": "PAYED",
            "FAILED": "FAILED",
            "RETURNED": "REFUNDED",
            "BLOCKED": "BLOCKED",
        }

        new_status = status_mapping.get(transaction_status, "PENDING")

        # Update payout status in the database
        update_paypal_payout_status(payout_item_id, new_status)
        logger.info("Updated payout status for payout_id: %s to %s", payout_item_id, new_status)

        return json.dumps({"message": "Webhook processed successfully."})

    except Exception as e:
        logger.error("Error processing PayPal webhook: %s", e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
