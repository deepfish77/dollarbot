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


@create_db_table
def create_table_from_schema():
    # Set the schema name and execute manually
    return BOT_PAYOUT_SCHEMA

create_table_from_schema()