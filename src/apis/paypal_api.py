import logging
import os
import requests
import boto3


logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


class PayPalApiService:
    """
    Handles PayPal API interactions (Sandbox or Production).
    """

    def __init__(self):
        self.ssm = boto3.client("ssm")
        self.stage = os.getenv("STAGE", "main")  # Default to "main"
        self.mode = self.get_ssm_parameter(
            f"/paypal/{self.stage}/mode"
        )  # Get mode from SSM

        # Select the correct credentials based on mode
        self.client_id = self.get_ssm_parameter(f"/paypal/{self.stage}/client_id")
        self.client_secret = self.get_ssm_parameter(
            f"/paypal/{self.stage}/client_secret"
        )

        # Set API URL based on mode
        self.base_url = (
            "https://api.sandbox.paypal.com"
            if self.mode == "sandbox"
            else "https://api.paypal.com"
        )

        self.access_token = self.get_access_token()

    def get_ssm_parameter(self, name):
        """
        Retrieve a secure parameter from AWS SSM Parameter Store.
        """
        response = self.ssm.get_parameter(Name=name, WithDecryption=True)
        return response["Parameter"]["Value"]

    def get_access_token(self):
        """
        Retrieve an access token from PayPal.
        """
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en_US"}
        auth = (self.client_id, self.client_secret)
        data = {"grant_type": "client_credentials"}

        response = requests.post(url, headers=headers, auth=auth, data=data, timeout=20)
        response.raise_for_status()

        access_token = response.json().get("access_token")
        logger.info("Successfully retrieved PayPal access token in %s mode.", self.mode)
        return access_token
