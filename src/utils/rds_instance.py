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

def _connect_to_rds_return_db_connector():
    rds_db = rds_connect.DbConnector(
        rds_pass,
        "postgres",
        "collabostartdb.cp4qoawi2ree.us-east-1.rds.amazonaws.com",
        "collaborone",
    )
    return rds_db



def get_rds_instance():
    return _connect_to_rds_return_db_connector()