import json
import psycopg2
import pandas as pd


class DbConnector:
    def __init__(self, password, user, host, db_name):

        self.password = password
        self.user = user
        self.db_name = db_name
        self.db_host = host

    def connect_to_db_return_connection(self):

        try:
            conn = psycopg2.connect(
                f"dbname={self.db_name} user={self.user} host={self.db_host} port='5432' password={self.password}"
            )
        except EnvironmentError as env_err:
            print("I am unable to connect to the database " + env_err)
        return conn

    def connect_to_db(self):

        connection = self.connect_to_db_return_connection()
        cur = connection.cursor()
        return cur

    def get_records(self, query):

        with self.connect_to_db() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            return records

    def get_records_headers(self, query):
        with self.connect_to_db() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description]  # Extract column names
            return {"headers": headers, "records": records}

    def get_records_json(self, query):
        with self.connect_to_db() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description]  # Extract column names
            # Convert to JSON format
            data = [dict(zip(headers, row)) for row in records]
            return json.dumps(data)  # Convert to JSON string

    def get_records_into_df(self, query):

        with self.connect_to_db() as cursor:
            cursor.execute(query)
            names = [x[0] for x in cursor.description]
            records = cursor.fetchall()
            returned_records = pd.DataFrame(records, columns=names)
            return returned_records

    def connect_to_db_update(self):
        connection = self.connect_to_db_return_connection()
        cur = connection.cursor()
        return cur, connection

    def update_records(self, query):
        cur, connection = self.connect_to_db_update()
        with cur as cursor:
            cursor.execute(query)
            commit_msg = connection.commit()
            return commit_msg
