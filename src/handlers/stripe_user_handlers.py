import json
from src.operations.stripe_connected_account import create_connected_account


def create_connected_account_handler(event, _):
    body = json.loads(event.get("body", "{}"))
    email = body.get("email")
    try:
        account = create_connected_account(email)
        print("the account that was created is: ", account)
        return {"statusCode": 200, "body": json.dumps({"account_id": account.id})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
