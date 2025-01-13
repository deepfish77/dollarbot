import logging
from src.queries.paypal_queries import store_paypal_user

# Initialize logger
logger = logging.getLogger(__name__)

class PayPalUserService:
    def create_user(self, user_id, paypal_email):
        """
        Create a PayPal user by storing their details in the database.
        """
        logger.info("Creating PayPal user for user_id: %s with email: %s", user_id, paypal_email)
        success = store_paypal_user(user_id, paypal_email)
        if success:
            logger.info("PayPal user created successfully for user_id: %s", user_id)
            return True
        else:
            logger.error("Failed to create PayPal user for user_id: %s", user_id)
            return False
