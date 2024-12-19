from src.queries.bot_initialized import get_order_by_id , create_transaction_for_user


def on_page_load_init(bot_id, user_id, order_id):

    # Get the order from bubble dbo
    received_order = get_order_by_id(bot_id=bot_id, order_external_id=order_id)
    print("received_order: ", received_order)
    # Check bot id and user id matchiing
    if received_order:
        create_transaction_for_user()
    # Create a new record of transaction in the local db

    # Set the bubble bot record to in progress
    # Charge the credit card
    # Set the transaction details into payment locally
    # preview the iframe of the bot
    # return true or false
