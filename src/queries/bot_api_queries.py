from src.utils.rds_instance import get_rds_instance as rds_connector


rds_db = rds_connector()


def create_bot_service(bot_id, bot_name, bot_external_id):
    query = f"""INSERT INTO bots.bot_service (bot_id,bot_name,bot_external_id)
    VALUES ('{bot_id}','{bot_name}','{bot_external_id}')"""
    try:
        rds_db.update_records(query)
        return True
    except Exception as e:
        print("Failed to create new bot service with exception: ", e)
        return False


def create_new_transaction(
    stripe_id, stripe_details, user_id, bot_id, transaction_status
):
    query = f"""INSERT INTO bots.bot_transactions (stripe_id,stripe_details,user_id,bot_id,transaction_status)
    VALUES ('{stripe_id}','{stripe_details}','{user_id}','{bot_id}','{transaction_status}')"""
    try:
        rds_db.update_records(query)
        return True
    except Exception as e:
        print("Failed to create new transaction for user with exception: ", e)
        return False


def create_new_bot_order(
    bot_name, bot_external_id, order_external_id, receipt_id, order_by, order_status
):
    query = f"""INSERT INTO bots.bot_order (bot_name, bot_external_id, order_external_id, receipt_id, order_by, order_status)
    VALUES ('{bot_name}','{bot_external_id}','{order_external_id}','{receipt_id}','{order_by}','{order_status}')"""
    print("query create_new_bot_order", query)
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




def get_transaction_by_id(order_external_id, bot_id):
    query = f"""SELECT * from bots.bot_transactions WHERE external_transaction_id ='{order_external_id}' and bot_id='{bot_id}' """
    records = rds_db.get_records_json(query=query)
    # print("records: ", records)
    return records


def get_order_by_id(order_external_id):
    query = f"""SELECT * from bots.bot_order WHERE order_external_id ='{order_external_id}'"""
    records = rds_db.get_records_json(query=query)
    print(f" query {query}, get_order_by_id records: ", records)
    return records


def update_order_status(order_external_id, order_status):
    query = f"""UPDATE bots.bot_order SET order_status = '{order_status}' where order_external_id = '{order_external_id}' """
    try:
        rds_db.update_records(query)
        return True
    except Exception as e:
        print(
            f"Failed to update {order_external_id} , order to status {order_status}, with exception:  ",
            e,
        )
        return False
