import logging
import stripe
import boto3
from typing import Optional, Dict

# Initialize AWS SSM client
ssm = boto3.client("ssm")
# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Fetch Stripe API key from SSM Parameter Store
try:
    # Make the parameters use environment variables
    stripe_api_key = ssm.get_parameter(Name="/stripe/secret_dev", WithDecryption=True)[
        "Parameter"
    ]["Value"]
    stripe.api_key = stripe_api_key
except Exception as e:

    raise RuntimeError(f"Error fetching Stripe API key from SSM: {e}")


class StripeTransferService:
    """
    A service class to manage Stripe transfers and payouts.
    """

    @staticmethod
    def create_transfer(
        amount: int,
        connected_account_id: str,
        currency: str = "usd",
        description: Optional[str] = None,
    ) -> Optional[str]:
        """
        Create a transfer to a connected account.

        :param amount: Amount to transfer in the smallest currency unit (e.g., cents).
        :param connected_account_id: The recipient's Stripe connected account ID.
        :param currency: The currency (default is USD).
        :param description: Optional description for the transfer.
        :return: The transfer ID if successful, None otherwise.
        """
        try:
            logger.info(
                "Creating transfer of %d %s to account %s",
                amount,
                currency,
                connected_account_id,
            )
            transfer = stripe.Transfer.create(
                amount=amount,
                currency=currency,
                destination=connected_account_id,
                description=description,
            )
            logger.info("Transfer created successfully: %s", transfer["id"])
            return transfer["id"]
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
