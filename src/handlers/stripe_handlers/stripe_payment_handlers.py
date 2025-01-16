# Lambda handler to create a transfer
import json
from src.operations.stripe_operations.stripe_transer import StripeTransferService


def create_transfer_handler(event, _):
   
    account_id = event["account_id"]
    amount = event["amount"]
    try:
        transfer = StripeTransferService.create_transfer(account_id, amount)
        return {"statusCode": 200, "body": json.dumps({"transfer_id": transfer.id})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
