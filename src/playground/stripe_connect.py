import json
import stripe
import os
import boto3

ssm = boto3.client("ssm")

stripe_api_key = ssm.get_parameter(Name="/stripe/secret_dev", WithDecryption=True)[
    "Parameter"
]["Value"]

stripe.api_key = stripe_api_key


# Function to generate an account onboarding link
def generate_account_link(account_id, refresh_url="", return_url=""):
    account_link = stripe.AccountLink.create(
        account=account_id,
        refresh_url=refresh_url,
        return_url=return_url,
        type="account_onboarding",
    )
    return account_link



# Lambda handler to generate an account onboarding link
def account_link_handler(account_id):
    try:
        account_link = generate_account_link(account_id)
        return account_link
    except Exception as e:
        return False



import logging
from typing import Optional, Dict
import boto3
import stripe


ssm = boto3.client("ssm")

stripe_api_key = ssm.get_parameter(Name="/stripe/secret_dev", WithDecryption=True)[
    "Parameter"
]["Value"]

# Set your Stripe secret key
stripe.api_key = stripe_api_key

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)



def create_stripe_transfer(
    amount: int, connected_account_id: str, description: Optional[str] = None, currency: str = "usd"
) -> Dict[str, Optional[str]]:
    """
    Create a single transfer to a connected account.

    :param amount: Amount to transfer in the smallest currency unit (e.g., cents for USD).
    :param currency: The currency (e.g., 'usd').
    :param connected_account_id: The recipient's Stripe connected account ID.
    :param description: Optional description for the transfer.
    :return: A dictionary with the transfer status and details.
    """
    # Input validation
    if amount <= 0:
        logger.error("Amount must be a positive integer.")
        return {"status": "failed", "error": "Invalid amount."}

    if not connected_account_id.startswith("acct_"):
        logger.error("Invalid connected account ID.")
        return {"status": "failed", "error": "Invalid connected account ID."}

    try:
        # Use an idempotency key to prevent duplicate transfers
        idempotency_key = f"transfer_{connected_account_id}_{amount}"

        # Create the transfer
        transfer = stripe.Transfer.create(
            amount=amount,
            currency=currency,
            destination=connected_account_id,
            description=description,
            idempotency_key=idempotency_key,
        )

        logger.info(f"Transfer successful: {transfer['id']}")
        return {"status": "success", "transfer_id": transfer['id']}

    except stripe.error.CardError as e:
        logger.error(f"Card error: {e.user_message}")
        return {"status": "failed", "error": e.user_message}

    except stripe.error.RateLimitError:
        logger.error("Rate limit error: Too many requests to Stripe API.")
        return {"status": "failed", "error": "Rate limit error."}

    except stripe.error.InvalidRequestError as e:
        logger.error(f"Invalid request: {e.user_message}")
        return {"status": "failed", "error": e.user_message}

    except stripe.error.AuthenticationError:
        logger.error("Authentication error: Invalid Stripe API key.")
        return {"status": "failed", "error": "Authentication error."}

    except stripe.error.APIConnectionError:
        logger.error("Network error: Failed to connect to Stripe.")
        return {"status": "failed", "error": "Network error."}

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e.user_message}")
        return {"status": "failed", "error": e.user_message}

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"status": "failed", "error": "Unexpected error."}
