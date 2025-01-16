from src.queries.bot_api_queries import create_new_transaction
from src.utils.enums import TRANSACTION_STATUS
import random
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

def generate_and_insert_transactions(user_id: str, bot_ids: list, num_transactions: int = 30):
    """
    Generates and inserts multiple transactions into the database using create_new_transaction.

    :param user_id: The user ID for which transactions will be generated.
    :param bot_ids: A list of bot IDs to associate with the transactions.
    :param num_transactions: Number of transactions to generate (default is 30).
    """
    for _ in range(num_transactions):
        payout_id = f"payout_{random.randint(100000, 999999)}"
        payout_details = f"details_{random.randint(1000, 9999)}"
        bot_id = random.choice(bot_ids)
        transaction_status = random.choice(list(TRANSACTION_STATUS)).value

        # Insert the transaction using create_new_transaction
        success = create_new_transaction(payout_id, payout_details, user_id, bot_id, transaction_status)
        if success:
            logger.info("Successfully created transaction: %s", payout_id)
        else:
            logger.error("Failed to create transaction: %s", payout_id)

# Example usage
if __name__ == "__main__":
    user_id = "deepfish.77@gmail.com"
    bot_ids = [
        "1735726614984x852533100107006000",
        "1735160980318x428924370341330940",
        "1735040959653x862285802586505200",
        "1735082849640x593340557411483600",
        "1735085719005x945294131110608900"
    ]
    generate_and_insert_transactions(user_id, bot_ids)
