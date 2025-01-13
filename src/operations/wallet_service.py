import logging
from src.queries.wallet_queries import check_balance, deposit, deduct

# Initialize logger
logger = logging.getLogger(__name__)


class WalletService:
    def check_balance(self, user_id):
        """Check the user's wallet balance."""
        balance = check_balance(user_id)
        logger.info("Checked balance for user_id: %s, balance: %s", user_id, balance)
        return balance

    def deposit(self, user_id, amount):
        """Deposit funds to the user's wallet."""
        success = deposit(user_id, amount)
        if success:
            logger.info("Deposited %s to user_id: %s", amount / 100, user_id)
        else:
            logger.error("Failed to deposit %s to user_id: %s", amount / 100, user_id)
        return success

    def deduct(self, user_id, amount):
        """Deduct funds from the user's wallet."""
        success = deduct(user_id, amount)
        if success:
            logger.info("Deducted %s from user_id: %s", amount / 100, user_id)
        else:
            logger.error("Failed to deduct %s from user_id: %s", amount / 100, user_id)
        return success
