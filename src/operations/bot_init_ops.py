import json
from src.utils.enums import ORDER_STATUS, TRANSACTION_STATUS
from src.apis.bubble_api import BubbleApiOperations
from src.queries.bot_api_queries import (
    get_order_by_id,
    update_order_status,
    create_new_transaction,
)
from src.utils.enums import ORDER_STATUS


class BotOrderOps:

    def __init__(self, bot_id, user_id):
        self.bot_id = bot_id
        self.user_id = user_id

    def order_received(self, order_id):
        # Check the order
        received_order = get_order_by_id(order_external_id=order_id)
        print(f"received_order from DB -id -{order_id} ---", received_order)

        if received_order:
            received_order_id = json.loads(received_order)[0].get("order_external_id")
            print("received order id, ", received_order_id)
            # Change the bot status to Started
            order_status_update = update_order_status(
                order_id, str(ORDER_STATUS.INITIALIZED.name)
            )

            order_status_update_bubble = BubbleApiOperations(
                "payments_all"
            ).update_bubble_object(
                order_id, "order_status", ORDER_STATUS.INITIALIZED.name
            )

            if (
                received_order_id == order_id
                and order_status_update
                and order_status_update_bubble
            ):
                print("order_status_update: ", order_status_update)
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
                response = {
                    "success": False,
                    "message": f"""Order id don't match source
                    received_order_id:{received_order_id},
                    order_status_update: {order_status_update},
                    order_status_update_bubble: {order_status_update_bubble}""",
                    "data": {
                        "bot_id": self.bot_id,
                        "user_id": self.user_id,
                        "order_id": order_id,
                    },
                }
        else:
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
        # Check the order
        completed_order = get_order_by_id(order_external_id=order_id)

        if completed_order:
            received_order_id = json.loads(completed_order)[0].get("order_external_id")
            if received_order_id == order_id:
                print("Order found")
                # Change the bot status to Completed and send to UI object in bubble
                update_order_status(order_id, ORDER_STATUS.ORDER_COMPLETED_BY_BOT.name)
                BubbleApiOperations("payments_all").update_bubble_object(
                    order_id, "order_status", ORDER_STATUS.ORDER_COMPLETED_BY_BOT.name
                )
                create_new_transaction(
                    stripe_id="123",
                    stripe_details="123",
                    user_id=self.user_id,
                    bot_id=self.bot_id,
                    transaction_status=TRANSACTION_STATUS.COMPLETED.name,
                )
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
            response = {
                "success": False,
                "message": "Order Didn't complete",
                "data": {
                    "bot_id": self.bot_id,
                    "user_id": self.user_id,
                    "order_id": order_id,
                },
            }

        # Return as JSON
        return response


# BotOrderOps(
#     bot_id="1733667359136x370884607558287360", user_id="shachar.czitron+123@gmail.com"
# ).order_received("1734622085967x741700514852634600")1735037803498x438172901858345000 
