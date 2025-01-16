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

USERS_SCHEMA_UPDATE_STRIPE = """ALTER TABLE users.users
ADD COLUMN stripe_account_id VARCHAR(50),
ADD COLUMN charges_enabled BOOLEAN DEFAULT FALSE,
ADD COLUMN payouts_enabled BOOLEAN DEFAULT FALSE,
ADD COLUMN account_status VARCHAR(20) DEFAULT 'pending',
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"""

EXTERNAL_ACCOUNTS = """CREATE TABLE bots.external_accounts (
    id SERIAL PRIMARY KEY,
    account_id VARCHAR(50) NOT NULL,
    external_account_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (account_id, external_account_id)
);
"""

COMLIANCE_ISSUES = """CREATE TABLE bots.compliance_issues (
    id SERIAL PRIMARY KEY,
    account_id VARCHAR(50) NOT NULL,
    issue_type VARCHAR(50) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (account_id, issue_type)
);"""


PAYPAL_BUNDLE = """-- Table for PayPal Users
CREATE TABLE paypal_users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL UNIQUE,
    paypal_email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for PayPal Transactions
CREATE TABLE bots.paypal_transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(255) NOT NULL UNIQUE,
    user_id VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for PayPal Payouts
CREATE TABLE bots.paypal_payouts (
    id SERIAL PRIMARY KEY,
    payout_id VARCHAR(255) NOT NULL UNIQUE,
    user_id VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Failed PayPal Payouts
CREATE TABLE bots.failed_paypal_payouts (
    id SERIAL PRIMARY KEY,
    payout_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    failure_reason TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for PayPal Disputes
CREATE TABLE bots.paypal_disputes (
    id SERIAL PRIMARY KEY,
    dispute_id VARCHAR(255) NOT NULL UNIQUE,
    user_id VARCHAR(255) NOT NULL,
    transaction_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
PAYPAL_FAILED_PAYOURS = """CREATE TABLE IF NOT EXISTS bots.failed_payouts (
    payout_id VARCHAR(255) PRIMARY KEY,      -- Unique ID for the payout
    user_id VARCHAR(255) NOT NULL,           -- The ID of the user who was supposed to receive the payout
    amount DECIMAL(10,2) NOT NULL,           -- The amount that was supposed to be paid
    failure_reason TEXT NOT NULL,            -- Reason why the payout failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Timestamp of failure
);
"""

@create_db_table
def create_table_from_schema():
    # Set the schema name and execute manually
    return PAYPAL_FAILED_PAYOURS


create_table_from_schema()
