from src.utils.rds_instance import get_rds_instance as rds_connector
import logging

# Initialize the RDS connection
rds_db = rds_connector()

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def get_completed_transactions_for_user(user_id):
    """
    Retrieves all transactions that are eligable for transfer funds

    :return: A list of transactions that the user can withdrawal.
    """
    query = f"""
        SELECT *
        FROM bots.bot_transactions
        WHERE transaction_status = 'COMPLETED'
        AND user_id = '{user_id}'
        ORDER BY transaction_id  DESC;
    """
    try:
        records = rds_db.get_records(query)
        logger.info("Successfully fetched eligible transactions for user: %s", user_id)
        return records
    except Exception as e:
        logger.error("Failed to fetch eligible transactions with exception : %s", e)
        return []


def get_transaction_by_id(order_external_id):
    """
    Retrieves  transactions that are eligable for transfer funds

    :return: A list of transactions that the user can withdrawal.
    """
    query = f"""SELECT * 
                FROM bots.bot_transactions 
                WHERE external_transaction_id ='{order_external_id}'
                """
    records = rds_db.get_records_json(query=query)
    # print("records: ", records)
    return records


def get_all_transactions_for_user(user_id):
    """
    Retrieves all transactions for a specific bot

     :return: A list of transactions for a specific bot.
    """
    query = f"""
        SELECT *
        FROM bots.bot_transactions
        WHERE  user_id = '{user_id}'
        ORDER BY transaction_id  DESC;
    """
    try:

        records = rds_db.get_records_into_df(query)
        logger.info("Successfully fetched  transactions for user_id: %s", user_id)
        return records

    except Exception as e:
        logger.error("Failed to fetch  transactions with exception : %s", e)
        return []



def update_transaction_status(transaction_id, transaction_status):
    """
    Update transaction status.
    """
    query = f"""
        UPDATE bots.bot_transactions
        SET transaction_status = {transaction_status}
        WHERE transaction_id = '{transaction_id}';
    """
    try:
        rds_db.update_records(query)
        logger.info(
            "Transaction: %s , Updated successfully to %s", transaction_id, transaction_status
        )
        return True
    except Exception as e:
        logger.error(
            "Failed transaction status update: %s ,with error %s", transaction_id, e
        )
        return False


def update_transaction_successful_dev_payout(
    transaction_id, payout_id, payout_details=None
):
    """
    Update transaction payed to user.
    """
    query = f"""
        UPDATE bots.transactions
        SET transaction_status = 'PAYED', updated_at = CURRENT_TIMESTAMP,
        payout_id = '{payout_id}'
        WHERE transaction_id = '{transaction_id}';
    """
    try:
        rds_db.update_records(query)
        logger.info(
            "Transaction: %s ,Payed successfully to %s", transaction_id, payout_id
        )
        return True
    except Exception as e:
        logger.error(
            "Failed transaction payment update: %s ,with error %s", transaction_id, e
        )
        return False
