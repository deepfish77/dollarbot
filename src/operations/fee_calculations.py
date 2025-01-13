def calculate_fee_with_platform_fee(
    amount: int,
    platform_fee_rate: float = 0.15,
) -> dict:
    """
    Calculates the Stripe fee and platform fee for a transaction, and returns a fee breakdown.

    :param amount: Transaction amount in the smallest currency unit (e.g., cents for USD).
    :param currency: The currency code (default is 'usd').
    :param payment_method: The payment method used (default is 'card').
    :param platform_fee_rate: The platform fee rate as a decimal (default is 0.15 for 15%).
    :return: A dictionary with the fee breakdown.
    """
    # Convert amount to dollars for clarity
    amount_in_dollars = amount / 100

    # Stripe processing fee (2.9% + $0.30)
    processing_fee = round(amount * 0.029 + 30, 2)

    # Platform fee (15% of the transaction amount)
    platform_fee = round(amount * platform_fee_rate, 2)

    # Net payout to the connected account
    net_payout = (amount - processing_fee - platform_fee) / 100

    # Prepare the fee breakdown
    fee_breakdown = {
        "transaction_amount": f"${amount_in_dollars:.2f}",
        "stripe_fee": f"${processing_fee / 100:.2f}",
        "platform_fee": f"${platform_fee / 100:.2f}",
        "net_payout": f"${net_payout:.2f}",
    }

    return fee_breakdown


def is_payout_eligible(balance: int, minimum_threshold: int = 5) -> bool:
    """
    Checks if a user is eligible for a payout based on their balance and the minimum threshold.

    :param balance: User's account balance in cents.
    :param minimum_threshold: Minimum balance required for a payout (default is $50).
    :return: True if eligible, False otherwise.
    """
    return balance >= minimum_threshold


def calculate_refund(amount: int, refund_amount: int, platform_fee_rate: float = 0.15):
    """
    Calculates the adjusted fees for a refund.

    :param amount: Original transaction amount in cents.
    :param refund_amount: Refund amount in cents.
    :param platform_fee_rate: The platform fee rate as a decimal (default is 0.15 for 15%).
    :return: A dictionary with the refund breakdown.
    """
    original_fee = round(amount * 0.029 + 30)
    platform_fee = round(amount * platform_fee_rate)
    refund_fee = round(refund_amount * 0.029 + 30)

    return {
        "original_fee": original_fee / 100,
        "platform_fee": platform_fee / 100,
        "refund_fee": refund_fee / 100,
        "net_refund": refund_amount / 100 - refund_fee / 100,
    }


def calculate_full_fee_breakdown(
    amount: int,
    currency: str = "usd",
    platform_fee_rate: float = 0.15,
    tax_rate: float = 0,
    conversion_fee_rate: float = 0.01,
):
    stripe_fee = round(amount * 0.029 + 30)
    platform_fee = round(amount * platform_fee_rate)
    tax = round(amount * tax_rate)
    conversion_fee = round(amount * conversion_fee_rate) if currency != "usd" else 0

    net_payout = amount - stripe_fee - platform_fee - tax - conversion_fee

    return {
        "transaction_amount": amount / 100,
        "stripe_fee": stripe_fee / 100,
        "platform_fee": platform_fee / 100,
        "tax": tax / 100,
        "conversion_fee": conversion_fee / 100,
        "net_payout": net_payout / 100,
    }
