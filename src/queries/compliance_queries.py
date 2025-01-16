from src.utils.rds_instance import get_rds_instance as rds_connector

# Initialize the RDS connection
rds_db = rds_connector()

import logging
logger = logging.getLogger(__name__)

def log_compliance_issue(account_id, issue_type, description):
    """
    Log a compliance issue in the database.
    """
    query = f"""
        INSERT INTO bots.compliance_issues (account_id, issue_type, description, status)
        VALUES ('{account_id}', '{issue_type}', '{description}', 'open')
        ON CONFLICT (account_id, issue_type)
        DO UPDATE SET description = '{description}', status = 'open', updated_at = CURRENT_TIMESTAMP;
    """
    try:
        rds_db.update_records(query)
        logger.info("Compliance issue logged for account_id: %s", account_id)
        return True
    except Exception as e:
        logger.error("Failed to log compliance issue for account_id: %s, exception: %s", account_id, e)
        return False

def resolve_compliance_issue(account_id, issue_type):
    """
    Mark a compliance issue as resolved.
    """
    query = f"""
        UPDATE bots.compliance_issues
        SET status = 'resolved', updated_at = CURRENT_TIMESTAMP
        WHERE account_id = '{account_id}' AND issue_type = '{issue_type}';
    """
    try:
        rds_db.update_records(query)
        logger.info("Compliance issue resolved for account_id: %s", account_id)
        return True
    except Exception as e:
        logger.error("Failed to resolve compliance issue for account_id: %s, exception: %s", account_id, e)
        return False
