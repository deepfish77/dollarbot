from src.utils.rds_instance import get_rds_instance as rds_connector

# Initialize the RDS connection
rds_db = rds_connector()

import logging

logger = logging.getLogger(__name__)


def create_paypal_transaction_query(transaction_id, user_id, amount, status):
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
        logger.error(
            "Failed to create PayPal transaction for user_id: %s, exception: %s",
            user_id,
            e,
        )
        return False


def update_paypal_transaction_status_query(transaction_id, status):
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
        logger.info(
            "Successfully updated status for transaction_id: %s", transaction_id
        )
        return True
    except Exception as e:
        logger.error(
            "Failed to update status for transaction_id: %s, exception: %s",
            transaction_id,
            e,
        )
        return False


def store_paypal_user(user_id, paypal_email):
    """
    Store PayPal user details in the database.
    """
    query = f"""
        INSERT INTO bots.paypal_users (user_id, paypal_email, created_at)
        VALUES ('{user_id}', '{paypal_email}', CURRENT_TIMESTAMP)
        ON CONFLICT (user_id)
        DO UPDATE SET paypal_email = '{paypal_email}', updated_at = CURRENT_TIMESTAMP;
    """
    try:
        rds_db.update_records(query)
        logger.info("Successfully stored PayPal user for user_id: %s", user_id)
        return True
    except Exception as e:
        logger.error(
            "Failed to store PayPal user for user_id: %s, exception: %s", user_id, e
        )
        return False


# ✅ Log PayPal Payout
def log_paypal_payout(payout_id, user_id, amount, status):
    """
    Logs a PayPal payout in the database.
    """
    query = f"""
        INSERT INTO bots.paypal_payouts (payout_id, user_id, amount, status, created_at)
        VALUES ('{payout_id}', '{user_id}', {amount}, '{status}', CURRENT_TIMESTAMP);
    """
    try:
        rds_db.update_records(query)
        logger.info("Successfully logged PayPal payout for user_id: %s", user_id)
        return True
    except Exception as e:
        logger.error(
            "Failed to log PayPal payout for user_id: %s, exception: %s", user_id, e
        )
        return False


# ✅ Log Failed PayPal Payout
def log_failed_paypal_payout(payout_id, user_id, amount, reason):
    """
    Logs a failed PayPal payout.
    """
    query = f"""
        INSERT INTO bots.failed_payouts (payout_id, user_id, amount, failure_reason, created_at)
        VALUES ('{payout_id}', '{user_id}', {amount}, '{reason}', CURRENT_TIMESTAMP)
        ON CONFLICT (payout_id) DO UPDATE 
        SET failure_reason = EXCLUDED.failure_reason, created_at = CURRENT_TIMESTAMP;
    """
    try:
        rds_db.update_records(query)
        logger.info("Logged failed PayPal payout: %s", payout_id)
        return True
    except Exception as e:
        logger.error("Failed to log failed PayPal payout: %s", e)
        return False


# ✅ Handle PayPal Dispute
def log_paypal_dispute_query(dispute_id, user_id, transaction_id, status, reason):
    """
    Logs a PayPal dispute in the database.
    """
    query = f"""
        INSERT INTO bots.paypal_disputes (dispute_id, user_id, transaction_id, status, reason, created_at)
        VALUES ('{dispute_id}', '{user_id}', '{transaction_id}', '{status}', '{reason}', CURRENT_TIMESTAMP);
    """
    try:
        rds_db.update_records(query)
        logger.info("Successfully logged PayPal dispute for user_id: %s", user_id)
        return True
    except Exception as e:
        logger.error(
            "Failed to log PayPal dispute for user_id: %s, exception: %s", user_id, e
        )
        return False


# ✅ Fetch PayPal User
def get_paypal_user_query(user_id):
    """
    Fetch PayPal user details from the database.
    """
    query = f"""
        SELECT * FROM bots.paypal_users WHERE user_id = '{user_id}';
    """
    try:
        result = rds_db.get_records(query)
        logger.info("Successfully fetched PayPal user for user_id: %s", user_id)
        return result
    except Exception as e:
        logger.error(
            "Failed to fetch PayPal user for user_id: %s, exception: %s", user_id, e
        )
        return None


def get_failed_payouts():
    """
    Retrieves all failed PayPal payouts from the database.
    """
    query = "SELECT payout_id, user_id, amount FROM bots.failed_payouts;"
    try:
        failed_payouts = rds_db.get_records_into_df(query)
        logger.info("Successfully fetched failed payouts.")
        return failed_payouts
    except Exception as e:
        logger.error("Failed to retrieve failed PayPal payouts: %s", e)
        return None

def get_failed_payouts_for_user(user_id):
    """
    Retrieves all failed PayPal payouts for a specific user from the database.
    """
    query = f"""
        SELECT payout_id, user_id, amount 
        FROM bots.failed_payouts 
        WHERE user_id = '{user_id}';
    """
    try:
        failed_payouts = rds_db.get_records_into_df(query)
        logger.info("Successfully fetched failed payouts for user: %s", user_id)
        return failed_payouts
    except Exception as e:
        logger.error("Failed to retrieve failed PayPal payouts for user: %s, error: %s", user_id, e)
        return None
