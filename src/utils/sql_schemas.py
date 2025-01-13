import boto3
import functools
from psycopg2 import sql
import src.utils.rds_connect as rds_connect

ssm = boto3.client("ssm")

rds_user = ssm.get_parameter(Name="/rds/user", WithDecryption=True)["Parameter"][
    "Value"
]
rds_pass = ssm.get_parameter(Name="/rds/password", WithDecryption=True)["Parameter"][
    "Value"
]


def create_db_table(func):
    """Wrapper Decorator for db tables creation"""

    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        query = func(*args, **kwargs)
        results = rds_db.update_records(query)
        print("results: ", results)
        return results

    return wrapper_decorator


rds_db = rds_connect.DbConnector(
    rds_pass,
    "postgres",
    "collabostartdb.cp4qoawi2ree.us-east-1.rds.amazonaws.com",
    "collaborone",
)


BOT_SERVICE_SCHEMA = """CREATE TABLE IF NOT EXISTS bots.bot_service (
    bot_id SERIAL PRIMARY KEY,
    bot_name VARCHAR(50) NOT NULL,
    bot_external_id VARCHAR(255),
    bot_creation_date TIMESTAMP
);"""


BOT_ORDER_SCHEMA = """CREATE TABLE IF NOT EXISTS bots.bot_order (
    order_id SERIAL PRIMARY KEY,
    bot_name VARCHAR(50) NOT NULL,
    bot_external_id VARCHAR(255),
    order_external_id VARCHAR(100),
    order_by VARCHAR(100)
);"""

BOT_TRANSACTIONS_SCHEMA = """CREATE TABLE IF NOT EXISTS bots.bot_transactions (
    transaction_id SERIAL PRIMARY KEY,
    stripe_id VARCHAR(50) NOT NULL,
    stripe_details VARCHAR(255)
);"""

BOT_PAYOUT_SCHEMA = """CREATE TABLE IF NOT EXISTS bots.bot_payout (
    payout_id SERIAL PRIMARY KEY,
    stripe_id VARCHAR(50) NOT NULL,
    stripe_details VARCHAR(255),
    withdrawal_amount VARCHAR(50)
);"""


BOT_COMPANY_PAYOUT_SCHEMA = """CREATE TABLE IF NOT EXISTS bots.company_payout (
    payout_id SERIAL PRIMARY KEY,
    stripe_id VARCHAR(50) NOT NULL,
    stripe_details VARCHAR(255),
    withdrawal_amount VARCHAR(50)
);"""

BOT_TRANSACTIONS_SCHEMA_UPDATE_1 = """ALTER TABLE bots.bot_transactions 
    ADD COLUMN user_id VARCHAR(255),
    ADD COLUMN bot_id VARCHAR(255),
    ADD COLUMN transaction_status VARCHAR(100)
;"""
BOT_TRANSACTIONS_SCHEMA_UPDATE_2 = """ALTER TABLE bots.bot_transactions
    ADD COLUMN external_transaction_id VARCHAR(100)
;"""
BOT_TRANSACTIONS_SCHEMA_UPDATE_3 = """ALTER TABLE bots.bot_transactions
    ADD COLUMN external_order_id VARCHAR(100)
;"""

COMPANY_PAYOUT_SCHEMA_UPDATE_1 = """ALTER TABLE bots.bot_transactions 
    ADD COLUMN user_id VARCHAR(255),
    ADD COLUMN bot_id VARCHAR(255),
    ADD COLUMN transaction_status VARCHAR(100)
;"""

BOT_ORDER_SCHEMA_1 = """ALTER TABLE bots.bot_order
    ADD COLUMN order_status VARCHAR(100)
;"""
BOT_ORDER_SCHEMA_2 = """ALTER TABLE bots.bot_order
    ADD COLUMN receipt_id VARCHAR(100)
;"""

TRANSFER_SCHEMA = """CREATE TABLE bots.transfers (
    id SERIAL PRIMARY KEY,
    customer_external_id VARCHAR(50) NOT NULL,
    transfer_id VARCHAR(50) NOT NULL,
    connected_account_id VARCHAR(50) NOT NULL,
    amount INTEGER NOT NULL,
    currency VARCHAR(10) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL,
    failure_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""


@create_db_table
def create_table_from_schema():
    # Set the schema name and execute manually
    return TRANSFER_SCHEMA

create_table_from_schema()