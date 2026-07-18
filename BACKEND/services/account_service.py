from datetime import datetime, timezone
from models import Customer, Transaction, db
import config


def deposit(customer_id: int, raw_amount):
    """
    Add funds to a customer's account.

    Returns (success: bool, message: str).
    """
    # --- Validate amount ---
    try:
        amount = float(raw_amount)
    except (TypeError, ValueError):
        return False, "Please enter a valid numeric amount."

    if amount <= 0:
        return False, "Deposit amount must be greater than zero."

    if amount > config.MAX_TRANSACTION_AMOUNT:
        return False, f"Single transaction limit is ${config.MAX_TRANSACTION_AMOUNT:,.2f}."

    # --- Update balance ---
    customer = db.session.get(Customer, customer_id)
    if customer is None:
        return False, "Customer account not found."

    customer.balance = round(customer.balance + amount, 2)

    txn = Transaction(
        customer_id=customer_id,
        transaction_type="deposit",
        amount=amount,
        timestamp=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    db.session.add(txn)
    db.session.commit()

    return True, f"Successfully deposited ${amount:,.2f}. New balance: ${customer.balance:,.2f}."


def withdraw(customer_id: int, raw_amount):
    """
    Deduct funds from a customer's account.

    Returns (success: bool, message: str).
    """
    # --- Validate amount ---
    try:
        amount = float(raw_amount)
    except (TypeError, ValueError):
        return False, "Please enter a valid numeric amount."

    if amount <= 0:
        return False, "Withdrawal amount must be greater than zero."

    if amount > config.MAX_TRANSACTION_AMOUNT:
        return False, f"Single transaction limit is ${config.MAX_TRANSACTION_AMOUNT:,.2f}."

    # --- Overdraft guard (always read fresh from DB) ---
    customer = db.session.get(Customer, customer_id)
    if customer is None:
        return False, "Customer account not found."

    if amount > customer.balance:
        return False, "Insufficient funds."

    customer.balance = round(customer.balance - amount, 2)

    txn = Transaction(
        customer_id=customer_id,
        transaction_type="withdrawal",
        amount=amount,
        timestamp=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    db.session.add(txn)
    db.session.commit()

    return True, f"Successfully withdrew ${amount:,.2f}. New balance: ${customer.balance:,.2f}."


def get_balance(customer_id: int) -> float:
    """Return the customer's current balance, read fresh from the database."""
    customer = db.session.get(Customer, customer_id)
    if customer is None:
        return 0.0
    return customer.balance


def get_recent_transactions(customer_id: int, limit: int = 10):
    """Return the most recent transactions for a customer, newest first."""
    return (
        Transaction.query.filter_by(customer_id=customer_id)
        .order_by(Transaction.timestamp.desc())
        .limit(limit)
        .all()
    )
