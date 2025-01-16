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
    stripe_api_key = ssm.get_parameter(Name="/stripe/secret_dev", WithDecryption=True)[
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

    @staticmethod
    def add_bank_account(
        account_id: str, country: str, currency: str, bank_account_details: Dict
    ) -> bool:
        """
        Add a bank account to a connected account.

        :param account_id: The ID of the connected account.
        :param country: The country where the bank account is based.
        :param currency: The currency of the bank account.
        :param bank_account_details: Dictionary containing the bank account details.
        :return: True if successful, False otherwise.
        """
        try:
            logger.info("Adding bank account to connected account: %s", account_id)
            stripe.Account.create_external_account(
                account_id,
                external_account={
                    "object": "bank_account",
                    "country": country,
                    "currency": currency,
                    "account_holder_name": bank_account_details["account_holder_name"],
                    "account_holder_type": bank_account_details["account_holder_type"],
                    "account_number": bank_account_details["account_number"],
                    "routing_number": bank_account_details.get("routing_number"),
                },
            )
            logger.info("Bank account added successfully to account: %s", account_id)
            return True
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return False

    @staticmethod
    def add_card(account_id: str, card_details: Dict) -> bool:
        """
        Add a debit card to a connected account.

        :param account_id: The ID of the connected account.
        :param card_details: Dictionary containing the card details.
        :return: True if successful, False otherwise.
        """
        try:
            logger.info("Adding card to connected account: %s", account_id)
            stripe.Account.create_external_account(
                account_id,
                external_account={
                    "object": "card",
                    "number": card_details["number"],
                    "exp_month": card_details["exp_month"],
                    "exp_year": card_details["exp_year"],
                    "cvc": card_details["cvc"],
                },
            )
            logger.info("Card added successfully to account: %s", account_id)
            return True
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return False

    @staticmethod
    def retrieve_external_accounts(account_id: str) -> Optional[Dict]:
        """
        Retrieve all external accounts (bank accounts and cards) linked to a connected account.

        :param account_id: The ID of the connected account.
        :return: A dictionary containing external accounts or None if an error occurs.
        """
        try:
            logger.info("Retrieving external accounts for account: %s", account_id)
            accounts = stripe.Account.retrieve(account_id).external_accounts
            logger.info(
                "External accounts retrieved successfully for account: %s", account_id
            )
            return accounts
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return None

    @staticmethod
    def generate_onboarding_link(account_id: str, refresh_url: str='url', return_url: str='url2'):
        """
        Generate a Stripe Express onboarding link for the user.
        """
        try:
            account_link = stripe.AccountLink.create(
                account=account_id,
                refresh_url=refresh_url,
                return_url=return_url,
                type="account_onboarding",
            )
            return account_link["url"]
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
            return None

