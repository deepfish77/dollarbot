import logging
import stripe
import boto3
from typing import Optional, Dict

# Initialize AWS SSM client
ssm = boto3.client("ssm")

# Fetch Stripe API key from SSM Parameter Store
try:
    stripe_api_key = ssm.get_parameter(Name="/stripe/api_key", WithDecryption=True)["Parameter"]["Value"]
    stripe.api_key = stripe_api_key
except Exception as e:
    raise RuntimeError(f"Error fetching Stripe API key from SSM: {e}")

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class StripeTransferService:
    """
    A service class to manage Stripe transfers and payouts.
    """

    @staticmethod
    def create_transfer(amount: int, connected_account_id: str, currency: str = "usd", description: Optional[str] = None) -> Optional[str]:
        """
        Create a transfer to a connected account.

        :param amount: Amount to transfer in the smallest currency unit (e.g., cents).
        :param connected_account_id: The recipient's Stripe connected account ID.
        :param currency: The currency (default is USD).
        :param description: Optional description for the transfer.
        :return: The transfer ID if successful, None otherwise.
        """
        try:
            logger.info("Creating transfer of %d %s to account %s", amount, currency, connected_account_id)
            transfer = stripe.Transfer.create(
                amount=amount,
                currency=currency,
                destination=connected_account_id,
                description=description
            )
            logger.info("Transfer created successfully: %s", transfer['id'])
            return transfer['id']
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return None

    @staticmethod
    def retrieve_transfer(transfer_id: str) -> Optional[Dict]:
        """
        Retrieve details of a specific transfer.

        :param transfer_id: The ID of the transfer.
        :return: A dictionary containing transfer details, or None if an error occurs.
        """
        try:
            logger.info("Retrieving transfer: %s", transfer_id)
            transfer = stripe.Transfer.retrieve(transfer_id)
            logger.info("Transfer retrieved successfully: %s", transfer_id)
            return transfer
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return None

    @staticmethod
    def list_transfers(limit: int = 10) -> Optional[Dict]:
        """
        List recent transfers made from the platform account.

        :param limit: The number of transfers to retrieve (default is 10).
        :return: A dictionary containing a list of transfers.
        """
        try:
            logger.info("Listing up to %d transfers", limit)
            transfers = stripe.Transfer.list(limit=limit)
            logger.info("Transfers listed successfully")
            return transfers
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return None

    @staticmethod
    def create_payout(amount: int, connected_account_id: str, currency: str = "usd", description: Optional[str] = None) -> Optional[str]:
        """
        Create a payout to a bank account or debit card from a connected account.

        :param amount: Amount to payout in the smallest currency unit (e.g., cents).
        :param connected_account_id: The Stripe connected account ID.
        :param currency: The currency (default is USD).
        :param description: Optional description for the payout.
        :return: The payout ID if successful, None otherwise.
        """
        try:
            logger.info("Creating payout of %d %s to account %s", amount, currency, connected_account_id)
            payout = stripe.Payout.create(
                amount=amount,
                currency=currency,
                destination=connected_account_id,
                description=description,
                stripe_account=connected_account_id
            )
            logger.info("Payout created successfully: %s", payout['id'])
            return payout['id']
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return None

    @staticmethod
    def check_balance() -> Optional[Dict]:
        """
        Check the balance of the platform account.

        :return: A dictionary containing balance details, or None if an error occurs.
        """
        try:
            logger.info("Checking platform account balance")
            balance = stripe.Balance.retrieve()
            logger.info("Balance retrieved successfully")
            return balance
        except stripe.error.StripeError as e:
            logger.error("Stripe API error: %s", e.user_message)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return None
