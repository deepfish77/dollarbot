import logging
import json
from src.utils.enums import ORDER_STATUS, TRANSACTION_STATUS
from src.apis.bubble_api import BubbleApiOperations
from src.queries.bot_api_queries import (
    get_order_by_id,
    update_order_status,
    create_new_transaction,
)

# Initialize logger
logger = logging.getLogger(__name__)

class BotOrderOps:
    def __init__(self, bot_id, user_id):
        self.bot_id = bot_id
        self.user_id = user_id

    def order_received(self, order_id):
        """
        Process an order when received.
        """
        logger.info("Processing order_received for order_id: %s", order_id)

        # Check the order
        received_order = get_order_by_id(order_external_id=order_id)
        logger.info("Received order from DB for order_id: %s", order_id)

        if received_order:
            received_order_id = json.loads(received_order)[0].get("order_external_id")
            logger.info("Parsed received_order_id: %s", received_order_id)

            # Change the bot status to Initialized
            order_status_update = update_order_status(order_id, ORDER_STATUS.INITIALIZED.name)
            logger.info("Order status updated in DB to: %s", ORDER_STATUS.INITIALIZED.name)

            order_status_update_bubble = BubbleApiOperations("payments_all").update_bubble_object(
                order_id, "order_status", ORDER_STATUS.INITIALIZED.name
            )
            logger.info("Order status updated in Bubble to: %s", ORDER_STATUS.INITIALIZED.name)

            if (
                received_order_id == order_id
                and order_status_update
                and order_status_update_bubble
            ):
                logger.info("Order successfully processed for order_id: %s", order_id)
                response = {
                    "success": True,
                    "message": "Order received successfully",
                    "data": {
                        "bot_id": self.bot_id,
                        "user_id": self.user_id,
                        "order_id": order_id,
                    },
                }
            else:
                logger.error(
                    "Order ID mismatch or status updates failed for order_id: %s. "
                    "received_order_id: %s, order_status_update: %s, order_status_update_bubble: %s",
                    order_id, received_order_id, order_status_update, order_status_update_bubble
                )
                response = {
                    "success": False,
                    "message": "Order ID mismatch or status updates failed.",
                    "data": {
                        "bot_id": self.bot_id,
                        "user_id": self.user_id,
                        "order_id": order_id,
                    },
                }
        else:
            logger.error("Order not found for order_id: %s", order_id)
            response = {
                "success": False,
                "message": "Order not found",
                "data": {
                    "bot_id": self.bot_id,
                    "user_id": self.user_id,
                    "order_id": order_id,
                },
            }

        # Return as JSON
        return response

    def order_completed(self, order_id):
        """
        Process an order when completed.
        """
        logger.info("Processing order_completed for order_id: %s", order_id)

        # Check the order
        completed_order = get_order_by_id(order_external_id=order_id)
        logger.info("Order fetched from DB for order_id: %s", order_id)

        if completed_order:
            received_order_id = json.loads(completed_order)[0].get("order_external_id")
            logger.info("Parsed received_order_id: %s", received_order_id)

            if received_order_id == order_id:
                logger.info("Order found, updating status to Completed")

                # Change the bot status to Completed and update Bubble
                update_order_status(order_id, ORDER_STATUS.ORDER_COMPLETED_BY_BOT.name)
                logger.info("Order status updated in DB to: %s", ORDER_STATUS.ORDER_COMPLETED_BY_BOT.name)

                BubbleApiOperations("payments_all").update_bubble_object(
                    order_id, "order_status", ORDER_STATUS.ORDER_COMPLETED_BY_BOT.name
                )
                logger.info("Order status updated in Bubble to: %s", ORDER_STATUS.ORDER_COMPLETED_BY_BOT.name)

                # Create a new transaction
                create_new_transaction(
                    stripe_id="123",
                    stripe_details="123",
                    user_id=self.user_id,
                    bot_id=self.bot_id,
                    transaction_status=TRANSACTION_STATUS.COMPLETED.name,
                )
                logger.info("New transaction created for order_id: %s", order_id)

            response = {
                "success": True,
                "message": "Order Completed successfully",
                "data": {
                    "bot_id": self.bot_id,
                    "user_id": self.user_id,
                    "order_id": order_id,
                },
            }
        else:
            logger.error("Order not completed for order_id: %s", order_id)
            response = {
                "success": False,
                "message": "Order didn't complete",
                "data": {
                    "bot_id": self.bot_id,
                    "user_id": self.user_id,
                    "order_id": order_id,
                },
            }

        # Return as JSON
        return response
