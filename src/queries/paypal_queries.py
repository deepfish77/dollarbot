from src.utils.rds_instance import get_rds_instance as rds_connector

# Initialize the RDS connection
rds_db = rds_connector()

import logging
logger = logging.getLogger(__name__)

def create_paypal_transaction(transaction_id, user_id, amount, status):
    """
    Creates a new PayPal transaction record in the database.
    """
    query = f"""
        INSERT INTO bots.paypal_transactions (transaction_id, user_id, amount, status)
        VALUES ('{transaction_id}', '{user_id}', {amount}, '{status}');
    """
    try:
        rds_db.update_records(query)
        logger.info("Successfully created PayPal transaction for user_id: %s", user_id)
        return True
    except Exception as e:
        logger.error("Failed to create PayPal transaction for user_id: %s, exception: %s", user_id, e)
        return False


def update_paypal_transaction_status(transaction_id, status):
    """
    Updates the status of a PayPal transaction in the database.
    """
    query = f"""
        UPDATE bots.paypal_transactions
        SET status = '{status}', updated_at = CURRENT_TIMESTAMP
        WHERE transaction_id = '{transaction_id}';
    """
    try:
        rds_db.update_records(query)
        logger.info("Successfully updated status for transaction_id: %s", transaction_id)
        return True
    except Exception as e:
        logger.error("Failed to update status for transaction_id: %s, exception: %s", transaction_id, e)
        return False

def store_paypal_user(user_id, paypal_email):
    """
    Store PayPal user details in the database.
    """
    query = f"""
        INSERT INTO paypal_users (user_id, paypal_email, created_at)
        VALUES ('{user_id}', '{paypal_email}', CURRENT_TIMESTAMP)
        ON CONFLICT (user_id)
        DO UPDATE SET paypal_email = '{paypal_email}', updated_at = CURRENT_TIMESTAMP;
    """
    try:
        rds_db.update_records(query)
        logger.info("Successfully stored PayPal user for user_id: %s", user_id)
        return True
    except Exception as e:
        logger.error("Failed to store PayPal user for user_id: %s, exception: %s", user_id, e)
        return False