import requests
import logging
import boto3

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

class PayPalApiService:
    """
    Handles PayPal API interactions for account linking and payments.
    """

    def __init__(self, mode="sandbox"):
        self.ssm = boto3.client("ssm")
        self.client_id = self.get_ssm_parameter("/paypal/client_id")
        self.client_secret = self.get_ssm_parameter("/paypal/client_secret")
        self.base_url = "https://api.sandbox.paypal.com" if mode == "sandbox" else "https://api.paypal.com"

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

        response = requests.post(url, headers=headers, auth=auth, data=data)
        response.raise_for_status()

        access_token = response.json().get("access_token")
        logger.info("Successfully retrieved PayPal access token.")
        return access_token

    def create_partner_referral(self, user_id):
        """
        Create a partner referral link to onboard a user to PayPal.
        """
        url = f"{self.base_url}/v2/customer/partner-referrals"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        payload = {
            "tracking_id": user_id,
            "operations": [
                {
                    "operation": "API_INTEGRATION",
                    "api_integration_preference": {
                        "rest_api_integration": {
                            "integration_method": "PAYPAL",
                            "integration_type": "THIRD_PARTY",
                            "third_party_details": {
                                "features": ["PAYMENT", "REFUND"],
                            },
                        }
                    },
                }
            ],
            "partner_config_override": {
                "return_url": "https://your-platform.com/onboarding-success",
                "return_url_description": "The URL to return the merchant after PayPal onboarding.",
            },
            "products": ["EXPRESS_CHECKOUT"],
            "legal_consents": [
                {
                    "type": "SHARE_DATA_CONSENT",
                    "granted": True,
                }
            ],
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        referral_url = response.json().get("links", [])[1]["href"]
        logger.info("Successfully created partner referral link.")
        return referral_url
