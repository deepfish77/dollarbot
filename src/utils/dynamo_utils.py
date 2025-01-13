import boto3

session = boto3.resource("dynamodb")


def get_by_id(key_id, key, table_name):

    table = session.Table(table_name)
    returned_question = table.get_item(Key={key: key_id})
    print("question", returned_question)
    return returned_question


# get_user("deepfish+123@gmail.com")


def add_ledger(previous, current, obj, table_name="transactions_ledger"):
    table = session.Table(table_name)
    table.put_item(
        Item={
            "previous": previous,
            "current": current,
            "object": obj,
        }
    )
