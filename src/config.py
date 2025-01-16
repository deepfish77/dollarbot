import os

class Config:
    """
    Centralized configuration class for managing environment variables.
    """

    STAGE = os.getenv("STAGE", "dev")

    # Base URLs
    PAYPAL_API_URL = (
        "https://api.sandbox.paypal.com" if STAGE == "dev" else "https://api.paypal.com"
    )
    STRIPE_API_URL = (
        "https://api.stripe.com/v1" if STAGE == "dev" else "https://api.stripe.com/v1"
    )

    # Webhook URLs
    WEBHOOK_RETURN_URL = os.getenv(
        "WEBHOOK_RETURN_URL",
        "https://dev.your-platform.com/webhook" if STAGE == "dev" else "https://your-platform.com/webhook"
    )

    # Return URLs for user redirection
    RETURN_URL = os.getenv(
        "RETURN_URL",
        "https://dev.your-platform.com/return" if STAGE == "dev" else "https://your-platform.com/return"
    )

    # Other URLs
    PARTNER_REFERRAL_URL = f"{PAYPAL_API_URL}/v2/customer/partner-referrals"

    @staticmethod
    def get_config():
        """
        Returns the current configuration based on the environment.
        """
        return {
            "STAGE": Config.STAGE,
            "PAYPAL_API_URL": Config.PAYPAL_API_URL,
            "STRIPE_API_URL": Config.STRIPE_API_URL,
            "WEBHOOK_RETURN_URL": Config.WEBHOOK_RETURN_URL,
            "RETURN_URL": Config.RETURN_URL,
            "PARTNER_REFERRAL_URL": Config.PARTNER_REFERRAL_URL,
        }
