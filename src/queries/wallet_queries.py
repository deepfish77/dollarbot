import logging
from src.utils.rds_instance import get_rds_instance as rds_connector

rds_db = rds_connector()

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def check_balance(user_id):
    query = f"""
        SELECT balance 
        FROM bots.wallets 
        WHERE user_id = '{user_id}';
    """
    try:
        result = rds_db.get_records(query)
        balance = result[0][0] if result else 0
        logger.info(
            "Successfully checked balance for user_id: %s, balance: %s",
            user_id,
            balance,
        )
        return balance
    except Exception as e:
        logger.error(
            "Failed to check balance for user_id: %s with exception: %s", user_id, e
        )
        return 0


def deposit(user_id, amount):
    query = f"""
        INSERT INTO bots.wallets (user_id, balance)
        VALUES ('{user_id}', {amount})
        ON CONFLICT (user_id)
        DO UPDATE SET balance = wallets.balance + {amount}, updated_at = CURRENT_TIMESTAMP;
    """
    try:
        rds_db.update_records(query)
        logger.info("Successfully deposited %s to user_id: %s", amount / 100, user_id)
        return True
    except Exception as e:
        logger.error(
            "Failed to deposit funds for user_id: %s with exception: %s", user_id, e
        )
        return False


def deduct(user_id, amount):
    query = f"""
        UPDATE bots.wallets
        SET balance = balance - {amount}, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = '{user_id}' AND balance >= {amount};
    """
    try:
        rds_db.update_records(query)
        logger.info("Successfully deducted %s from user_id: %s", amount / 100, user_id)
        return True
    except Exception as e:
        logger.error(
            "Failed to deduct funds for user_id: %s with exception: %s", user_id, e
        )
        return False
