from src.utils.rds_instance import get_rds_instance as rds_connector
from src.utils.enums import TransferStatus


rds_db = rds_connector()


def insert_transfer(
    transfer_id,
    connected_account_id,
    amount,
    status,
    failure_reason=None,
    description="",
    currency="usd",
):
    """
    Inserts a record into the transfers table.
    """
    query = f"""
        INSERT INTO transfers (transfer_id, connected_account_id, amount, currency, description, status, failure_reason)
        VALUES ('{transfer_id}', '{connected_account_id}', {amount}, '{currency}', '{description}', '{status}', '{failure_reason}');
    """
    try:
        rds_db.update_records(query)
        return True
    except Exception as e:
        print("Failed to insert transfer record with the exception: ", e)
        return False


def update_transfer_status(transfer_id: str, status: TransferStatus):
    """
    Updates the status of a transfer record in the database.

    :param transfer_id: The Stripe transfer ID.
    :param status: The new status from TransferStatus Enum.
    :return: True if the update was successful, False otherwise.
    """
    query = f"""
        UPDATE transfers
        SET status = '{status.value}', updated_at = CURRENT_TIMESTAMP
        WHERE transfer_id = '{transfer_id}';
    """
    try:
        rds_db.update_records(query)
        return True
    except Exception as e:
        print("Failed to update transfer status with the exception: ", e)
        return False


def retrieve_transfer(transfer_id: str):
    """
    Retrieves a transfer record from the database by transfer_id.

    :param transfer_id: The Stripe transfer ID.
    :return: The transfer record as a dictionary, or None if not found.
    """
    query = f"""
        SELECT * FROM transfers
        WHERE transfer_id = '{transfer_id}';
    """
    try:
        result = rds_db.get_records(query)
        return result[0] if result else None
    except Exception as e:
        print("Failed to retrieve transfer record with the exception: ", e)
        return None


def list_transfers(connected_account_id: str):
    """
    Lists all transfers associated with a specific connected account.

    :param connected_account_id: The Stripe connected account ID.
    :return: A list of transfer records.
    """
    query = f"""
        SELECT * FROM transfers
        WHERE connected_account_id = '{connected_account_id}'
        ORDER BY created_at DESC;
    """
    try:
        return rds_db.get_records(query)
    except Exception as e:
        print("Failed to list transfers with the exception: ", e)
        return []


def count_transfers_by_status(status: TransferStatus):
    """
    Counts the number of transfers with a specific status.

    :param status: The status to count (from TransferStatus Enum).
    :return: The count of transfers with the given status.
    """
    query = f"""
        SELECT COUNT(*) FROM transfers
        WHERE status = '{status.value}';
    """
    try:
        result = rds_db.get_records(query)
        return result[0][0] if result else 0
    except Exception as e:
        print("Failed to count transfers by status with the exception: ", e)
        return 0


def get_total_amount_transferred(connected_account_id: str):
    """
    Calculates the total amount transferred to a specific connected account.

    :param connected_account_id: The Stripe connected account ID.
    :return: The total amount transferred in cents.
    """
    query = f"""
        SELECT SUM(amount) FROM transfers
        WHERE connected_account_id = '{connected_account_id}'
        AND status = 'completed';
    """
    try:
        result = rds_db.get_records(query)
        return result[0][0] if result else 0
    except Exception as e:
        print("Failed to get total amount transferred with the exception: ", e)
        return 0


def get_failed_transfers():
    """
    Retrieves all failed transfers along with their failure reasons.

    :return: A list of failed transfer records.
    """
    query = """
        SELECT transfer_id, connected_account_id, amount, failure_reason
        FROM transfers
        WHERE status = 'failed'
        ORDER BY created_at DESC;
    """
    try:
        return rds_db.get_records(query)
    except Exception as e:
        print("Failed to get failed transfers with the exception: ", e)
        return []
