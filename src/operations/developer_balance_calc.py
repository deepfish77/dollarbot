import logging
import pandas as pd

from src.queries.developer_payout_queries import (
    get_completed_transactions_for_user,
    get_all_transactions_for_user,
)

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


class DeveloperBalanceService:
    """
    Service to handle user balance, transaction history, and failed transactions.
    """

    def get_developer_balance(self, user_id):
        """
        Calculate the user's actual balance from eligible transactions after fees and deductions.

        :param user_id: The user ID for which the balance will be calculated.
        :return: A dictionary with the calculated balance and detailed breakdown.
        """
        # Step 1: Retrieve completed transactions
        transactions = get_completed_transactions_for_user(user_id)

        if not transactions:
            logger.info("No completed transactions found for user_id: %s", user_id)
            return {"balance": 0.00, "breakdown": "No transactions available."}

        # Step 2: Calculate total balance (1$ per transaction)
        total_earnings = sum([1 for _ in transactions])  # Each transaction is worth 1$

        # Step 3: Deduct PayPal fees (standard fee: 2.9% + $0.30 per transaction)
        num_transactions = len(transactions)
        paypal_fee_total = (total_earnings * 0.055) + (0.05 * num_transactions)

        # Step 4: Deduct ServiBots platform fee (15%)
        platform_fee_total = total_earnings * 0.15

        # Step 5: Calculate the actual balance after deductions
        actual_balance = total_earnings - paypal_fee_total - platform_fee_total

        # Step 6: Log the calculations
        logger.info("Successfully retrieved balance")

        # Step 7: Return the breakdown to the user
        return {
            "total_earnings": round(total_earnings, 2),
            "paypal_fee": round(paypal_fee_total, 2),
            "platform_fee": round(platform_fee_total, 2),
            "balance": round(actual_balance, 2),
        }


    def get_transaction_history(self, user_id):
        """
        Get the full transaction history for the user, including successful, pending, and failed transactions.
        Uses Pandas for data processing.
        """
        transactions_df = get_all_transactions_for_user(user_id)

        if transactions_df.empty:
            logger.info("No transactions found for user_id: %s", user_id)
            return {"success": False, "message": "No transaction history found."}

        # Log the retrieved transactions
        logger.info("Transactions found for user_id %s:\n%s", user_id, transactions_df)

        # Filter transactions by status using Pandas
        successful = transactions_df[
            transactions_df["transaction_status"].str.upper() == "PAYED"
        ].to_dict(orient="records")
        pending = transactions_df[
            transactions_df["transaction_status"].str.upper() == "COMPLETED"
        ].to_dict(orient="records")
        failed = transactions_df[
            transactions_df["transaction_status"].str.upper().isin(["FAILED", "BOT_FAILED"])
        ].to_dict(orient="records")

        return {
            "successful": successful,
            "pending": pending,
            "failed": failed,
        }

    def get_failed_transactions(self, user_id):
        """
        Get the user's failed transactions.
        """
        transactions = get_all_transactions_for_user(user_id)
        failed_transactions = [
            tx for tx in transactions if tx["transaction_status"] == "FAILED"
        ]

        if not failed_transactions:
            logger.info("No failed transactions found for user_id: %s", user_id)
            return {"success": False, "message": "No failed transactions found."}

        logger.info("Fetched failed transactions for user_id: %s", user_id)
        return failed_transactions
