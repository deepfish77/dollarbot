import logging
from typing import Optional, Dict
import stripe
import boto3

ssm = boto3.client("ssm")
# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Fetch Stripe API key from SSM Parameter Store
try:
    stripe_api_key = ssm.get_parameter(Name="/stripe/api_key", WithDecryption=True)[
        "Parameter"
    ]["Value"]
    stripe.api_key = stripe_api_key
except Exception as e:
    logger.error(f"Error fetching Stripe API key from SSM:{e}")
    raise RuntimeError(f"Error fetching Stripe API key from SSM: {e}")


class StripeConnectedAccountService:
    """
    A service class to manage Stripe connected accounts.
    """

    @staticmethod
    def create_connected_account(email: str) -> Optional[str]:
        """
        Create a new connected account.

        :param email: The email address of the user.
        :return: The connected account ID if successful, None otherwise.
        """
        if not email or "@" not in email:
            logger.error("Invalid email address provided: %s", email)
            return None

        try:
            logger.info("Creating connected account for email: %s", email)
            idempotency_key = f"create_connected_account_{email}"
            account = stripe.Account.create(
                type="express", email=email, idempotency_key=idempotency_key
            )
            logger.info("Connected account created successfully: %s", account["id"])
            return account["id"]
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return None

    @staticmethod
    def update_connected_account(account_id: str, update_data: Dict) -> bool:
        """
        Update an existing connected account.

        :param account_id: The ID of the connected account.
        :param update_data: A dictionary of fields to update.
        :return: True if the update was successful, False otherwise.
        """
        try:
            logger.info("Updating connected account: %s", account_id)
            stripe.Account.modify(account_id, **update_data)
            logger.info("Connected account updated successfully: %s", account_id)
            return True
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return False

    @staticmethod
    def retrieve_connected_account(account_id: str) -> Optional[Dict]:
        """
        Retrieve the details of a connected account.

        :param account_id: The ID of the connected account.
        :return: A dictionary containing account details, or None if an error occurs.
        """
        try:
            logger.info("Retrieving connected account: %s", account_id)
            account = stripe.Account.retrieve(account_id)
            logger.info("Connected account retrieved successfully: %s", account_id)
            return account
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return None

    @staticmethod
    def check_account_verification_status(account_id: str) -> Optional[bool]:
        """
        Check if a connected account is fully verified.

        :param account_id: The ID of the connected account.
        :return: True if the account is verified, False if not, or None if an error occurs.
        """
        account = StripeConnectedAccountService.retrieve_connected_account(account_id)
        if account:
            return account.get("charges_enabled", False)
        return None
