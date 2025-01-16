import logging
from src.queries.paypal_queries import (
    store_paypal_user,
    get_paypal_user_query
)
from src.apis.paypal_api import PayPalApiService

# Initialize logger
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

class PayPalUserService:
    """
    Service to handle PayPal user operations, including account linking, payouts, and disputes.
    """

    def __init__(self):
        self.paypal_api = PayPalApiService()

    def create_user(self, user_id, paypal_email):
        # Don't use this - > fix
        """
        Create a PayPal user by storing their details in the database.
        """
        logger.info("Creating PayPal user for user_id: %s with email: %s", user_id, paypal_email)
        success = store_paypal_user(user_id, paypal_email)
        if success:
            logger.info("PayPal user created successfully for user_id: %s", user_id)
            return {"success": True, "message": "PayPal user created successfully."}
        else:
            logger.error("Failed to create PayPal user for user_id: %s", user_id)
            return {"success": False, "message": "Failed to create PayPal user."}

    def link_paypal_account(self, user_id, paypal_email):
        """
        Link a PayPal account by verifying it through PayPal Webhooks and storing it in the database.
        """
        logger.info("Linking PayPal account for user_id: %s with email: %s", user_id, paypal_email)

        # Simulate account creation process
        self.create_user(user_id, paypal_email)

        logger.info("PayPal account linked for user_id: %s. Waiting for verification via webhook.", user_id)
        return {"success": True, "message": "PayPal account linked successfully. Awaiting verification."}

    def handle_webhook_event(self, event):
        """
        Handle PayPal Webhook events to verify accounts.
        """
        event_type = event.get("event_type")
        resource = event.get("resource")

        # Check if the event is a payment or payout confirmation
        if event_type in ["PAYMENT.SALE.COMPLETED", "PAYMENT.PAYOUTS-ITEM.SUCCEEDED"]:
            logger.info("Webhook event received: %s", event_type)
            user_id = resource.get("custom", "")  # Assuming you pass user_id in the custom field

            if user_id:
                self.mark_account_verified(user_id)
                logger.info("PayPal account verified for user_id: %s", user_id)
                return {"success": True, "message": f"PayPal account verified for user_id: {user_id}"}
            else:
                logger.error("User ID not found in webhook event.")
                return {"success": False, "message": "User ID not found in webhook event."}
        else:
            logger.warning("Unhandled webhook event type: %s", event_type)
            return {"success": False, "message": "Unhandled webhook event type."}

    def mark_account_verified(self, user_id):
        """
        Mark a PayPal account as verified in the database.
        """
        logger.info("Marking PayPal account as verified for user_id: %s", user_id)
        user = get_paypal_user_query(user_id)
        if user:
            update_status = store_paypal_user(user_id, user["paypal_email"])
            if update_status:
                logger.info("Successfully marked PayPal account as verified for user_id: %s", user_id)
                return True
        logger.error("Failed to mark PayPal account as verified for user_id: %s", user_id)
        return False
