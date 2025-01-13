import paypalrestsdk
import logging
from src.queries.paypal_queries import create_paypal_transaction, update_paypal_transaction_status

# Initialize logger
logger = logging.getLogger(__name__)

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": "your_paypal_client_id",
    "client_secret": "your_paypal_client_secret"
})


class PayPalService:
    def create_transaction(self, user_id, amount):
        """
        Create a new PayPal payment and record the transaction in the database.
        """
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": f"{amount:.2f}", "currency": "USD"},
                "description": f"Payment for user {user_id}"
            }],
            "redirect_urls": {
                "return_url": "https://your-return-url.com",
                "cancel_url": "https://your-cancel-url.com"
            }
        })

        if payment.create():
            transaction_id = payment.id
            create_paypal_transaction(transaction_id, user_id, amount, "pending")
            logger.info("Created PayPal payment with transaction_id: %s for user_id: %s", transaction_id, user_id)
            return payment.links[1].href  # Return approval URL
        else:
            logger.error("Failed to create PayPal payment for user_id: %s, error: %s", user_id, payment.error)
            return None

    def update_transaction_status(self, transaction_id, status):
        """
        Update the status of a PayPal transaction in the database.
        """
        return update_paypal_transaction_status(transaction_id, status)
