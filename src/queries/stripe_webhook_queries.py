import logging
from src.utils.rds_instance import get_rds_instance as rds_connector


# Initialize the RDS connection
rds_db = rds_connector()

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def log_failed_payout(account_id, payout_id, failure_reason):
    """
    Log a failed payout in the database.
    """
    query = f"""
        INSERT INTO bots.failed_payouts (account_id, payout_id, failure_reason)
        VALUES ('{account_id}', '{payout_id}', '{failure_reason}')
        ON CONFLICT (payout_id)
        DO UPDATE SET failure_reason = '{failure_reason}', retry_count = retry_count + 1, updated_at = CURRENT_TIMESTAMP;
    """
    try:
        rds_db.update_records(query)
        logger.info("Successfully logged failed payout: %s", payout_id)
        return True
    except Exception as e:
        logger.error("Failed to log failed payout: %s, exception: %s", payout_id, e)
        return False
