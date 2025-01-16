import json
from src.operations.stripe_webhook import StripeWebhookService

def compliance_handler(event, _):
    """
    Lambda handler to process Stripe compliance-related webhooks.
    """
    try:
        # Parse the Stripe event from the webhook
        stripe_event = json.loads(event["stripe_event"])
        response = StripeWebhookService.process_webhook(stripe_event)

        return {
            "statusCode": 200,
            "body": json.dumps(response),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": str(e)}),
        }
