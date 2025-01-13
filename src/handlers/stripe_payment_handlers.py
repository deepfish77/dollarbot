# Lambda handler to create a transfer
import json
from src.operations.stripe_transer import StripeTransferService


def create_transfer_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    account_id = body.get("account_id")
    amount = body.get("amount")
    try:
        transfer = StripeTransferService.create_transfer(account_id, amount)
        return {"statusCode": 200, "body": json.dumps({"transfer_id": transfer.id})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
