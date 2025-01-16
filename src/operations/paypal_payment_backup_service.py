import paypalrestsdk
import logging
from src.queries.paypal_queries import (
    create_paypal_transaction_query,
    update_paypal_transaction_status_query,
    log_failed_paypal_payout_query,
    log_paypal_dispute_query,
)


# This is going to be handled by UI, this code is for backend operations in case
# that customers fail to purchase the servicce directly
# Initialize logger
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

# Configure PayPal SDK
paypalrestsdk.configure(
    {
        "mode": "sandbox",  # Change to "live" for production
        "client_id": "your_paypal_client_id",
        "client_secret": "your_paypal_client_secret",
    }
)


class PayPalService:
    """
    Service to handle PayPal transactions, including payment creation, refunds, disputes, and payout tracking.
    """

    def create_transaction(self, user_id, amount):
        """
        Create a new PayPal payment and record the transaction in the database.
        """
        payment = paypalrestsdk.Payment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "transactions": [
                    {
                        "amount": {"total": f"{amount:.2f}", "currency": "USD"},
                        "description": f"Payment for user {user_id}",
                    }
                ],
                "redirect_urls": {
                    "return_url": "https://your-return-url.com",
                    "cancel_url": "https://your-cancel-url.com",
                },
            }
        )

        if payment.create():
            transaction_id = payment.id
            create_paypal_transaction_query(transaction_id, user_id, amount, "pending")
            logger.info(
                "Created PayPal payment with transaction_id: %s for user_id: %s",
                transaction_id,
                user_id,
            )
            return payment.links[1].href  # Return approval URL
        else:
            logger.error(
                "Failed to create PayPal payment for user_id: %s, error: %s",
                user_id,
                payment.error,
            )
            return None

    def update_paypal_transaction_status(self, transaction_id, status):
        """
        Update the status of a PayPal transaction in the database.
        """
        return update_paypal_transaction_status_query(transaction_id, status)

    def refund_paypal_transaction(self, transaction_id):
        """
        Refund a PayPal transaction.
        """
        try:
            payment = paypalrestsdk.Payment.find(transaction_id)
            if payment.refund():
                update_paypal_transaction_status_query(transaction_id, "refunded")
                logger.info("Successfully refunded transaction_id: %s", transaction_id)
                return {
                    "success": True,
                    "message": "Transaction refunded successfully.",
                }
            else:
                logger.error("Failed to refund transaction_id: %s", transaction_id)
                return {"success": False, "message": "Refund failed."}
        except Exception as e:
            logger.error(
                "Exception occurred while refunding transaction_id: %s, error: %s",
                transaction_id,
                e,
            )
            return {"success": False, "message": str(e)}

    def handle_dispute(self, dispute_id, user_id, transaction_id, reason):
        """
        Handle a PayPal dispute and log it in the database.
        """
        try:
            log_paypal_dispute_query(dispute_id, user_id, transaction_id, "open", reason)
            logger.info(
                "Logged PayPal dispute with dispute_id: %s for transaction_id: %s",
                dispute_id,
                transaction_id,
            )
            return {"success": True, "message": "Dispute logged successfully."}
        except Exception as e:
            logger.error(
                "Failed to log PayPal dispute for dispute_id: %s, error: %s",
                dispute_id,
                e,
            )
            return {"success": False, "message": str(e)}

    def get_paypal_transaction_details(self, transaction_id):
        """
        Fetch details of a PayPal transaction.
        """
        try:
            payment = paypalrestsdk.Payment.find(transaction_id)
            return payment.to_dict()
        except Exception as e:
            logger.error(
                "Failed to fetch transaction details for transaction_id: %s, error: %s",
                transaction_id,
                e,
            )
            return None
