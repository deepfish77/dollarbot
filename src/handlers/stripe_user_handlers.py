import logging
import json
from src.operations.stripe_connected_account import StripeConnectedAccountService
from src.queries.stripe_ops_queries import insert_transfer
from src.queries.stripe_ops_queries import add_stripe_account_to_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def create_connected_account_handler(event, _):
    email = event["email"]
    try:
        # Create Stripe account and register backend
        account = StripeConnectedAccountService.create_connected_account(email)
        logger.info("Connected account created successfully in stripe: %s", account)
        print("the account that was created is: ", account)
        # Register the account in backend
        add_stripe_account_to_user(account=account,)

        return {"statusCode": 200, "body": json.dumps({"account_id": account.id})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
