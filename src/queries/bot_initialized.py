import json
from src.utils.rds_instance import get_rds_instance as rds_connector
from src.utils.data_utils import (
    set_results_json_api_resp,
    set_results_for_single_item_response,
)

rds_db = rds_connector()


def create_bot_service(bot_id, bot_name, bot_external_id):
    query = f"""INSERT INTO bots.bot_service (bot_id,bot_name,bot_external_id)
    VALUES ('{bot_id}','{bot_name}','{bot_external_id}')"""
    rds_db.update_records(query=query)


def create_transaction_for_user(
    transaction_id, stripe_id, stripe_details, user_id, bot_id, transaction_status
):
    query = f"""INSERT INTO bots.bot_service (transaction_id,stripe_id,stripe_details,user_id,bot_id,transaction_status)
    VALUES ('{transaction_id}','{stripe_id}','{stripe_details}','{user_id}','{bot_id}','{transaction_status}')"""
    try:
        rds_db.update_records(query)
        return True
    except Exception as e:
        print("Failed to create new transaction for user with exception: ", e)
        return False


def update_transaction_status(transaction_status, transaction_id):
    query = f"""UPDATE bots.bot_service SET transaction_status = '{transaction_status}' WHERE transaction_id = '{transaction_id}' """
    try:
        rds_db.update_records(query)
        return True
    except Exception as e:
        print("Failed to update transaction status with the exception: ", e)
        return False


def create_new_developer_payout(stripe_id, stripe_details, withdrawal_amount):
    query = f""" INSERT INTO bots.bot_payout (stripe_id,stripe_details,withdrawal_amount) 
    VALUES ('{stripe_id}','{stripe_details}','{withdrawal_amount}')"""
    try:
        rds_db.update_records(query)
        return True
    except Exception as e:
        print("Failed to create new developer payout with the exception: ", e)
        return False


# def update_developer_payment_status():
#     pass


def get_order_by_id(order_external_id, bot_id):
    query = f"""SELECT * from bots.bot_transactions WHERE external_transaction_id ='{order_external_id}' and bot_id='{bot_id}' """
    records = rds_db.get_records(query=query)
    print("records: ", records)
    return records
