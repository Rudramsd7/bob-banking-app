"""
Unit tests for services/account_service.py

Run from BACKEND/ with:  python -m pytest tests/ -v
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from flask import Flask
from werkzeug.security import generate_password_hash

from models import db, Customer, Transaction
from services.account_service import deposit, withdraw, get_balance


@pytest.fixture
def app():
    test_app = Flask(__name__)
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    test_app.config["SECRET_KEY"] = "test-secret"
    test_app.config["TESTING"] = True

    db.init_app(test_app)

    with test_app.app_context():
        db.create_all()
        customer = Customer(
            username="accuser",
            password_hash=generate_password_hash("pass"),
            name="Acc User",
            balance=1000.0,
        )
        db.session.add(customer)
        db.session.commit()

        yield test_app

        db.drop_all()


@pytest.fixture
def ctx(app):
    with app.app_context():
        yield


@pytest.fixture
def customer_id(ctx):
    customer = Customer.query.filter_by(username="accuser").first()
    return customer.id


# ---------------------------------------------------------------------------
# Deposit tests
# ---------------------------------------------------------------------------

class TestDeposit:

    def test_valid_deposit_increases_balance(self, ctx, customer_id):
        success, _ = deposit(customer_id, "200.00")
        assert success is True
        assert get_balance(customer_id) == pytest.approx(1200.0)

    def test_deposit_creates_transaction_record(self, ctx, customer_id):
        deposit(customer_id, "50.00")
        txn = Transaction.query.filter_by(customer_id=customer_id).first()
        assert txn is not None
        assert txn.transaction_type == "deposit"
        assert txn.amount == pytest.approx(50.0)

    def test_zero_deposit_rejected(self, ctx, customer_id):
        success, message = deposit(customer_id, "0")
        assert success is False
        assert "greater than zero" in message.lower()

    def test_negative_deposit_rejected(self, ctx, customer_id):
        success, _ = deposit(customer_id, "-100")
        assert success is False

    def test_non_numeric_deposit_rejected(self, ctx, customer_id):
        success, _ = deposit(customer_id, "abc")
        assert success is False

    def test_empty_amount_rejected(self, ctx, customer_id):
        success, _ = deposit(customer_id, "")
        assert success is False

    def test_over_limit_deposit_rejected(self, ctx, customer_id):
        success, _ = deposit(customer_id, "9999999")
        assert success is False


# ---------------------------------------------------------------------------
# Withdrawal tests
# ---------------------------------------------------------------------------

class TestWithdraw:

    def test_valid_withdrawal_decreases_balance(self, ctx, customer_id):
        success, _ = withdraw(customer_id, "300.00")
        assert success is True
        assert get_balance(customer_id) == pytest.approx(700.0)

    def test_withdrawal_creates_transaction_record(self, ctx, customer_id):
        withdraw(customer_id, "100.00")
        txn = Transaction.query.filter_by(
            customer_id=customer_id, transaction_type="withdrawal"
        ).first()
        assert txn is not None
        assert txn.amount == pytest.approx(100.0)

    def test_withdrawal_exceeding_balance_rejected(self, ctx, customer_id):
        success, message = withdraw(customer_id, "9999.00")
        assert success is False
        assert "insufficient" in message.lower()

    def test_balance_unchanged_after_failed_withdrawal(self, ctx, customer_id):
        before = get_balance(customer_id)
        withdraw(customer_id, "9999.00")
        assert get_balance(customer_id) == pytest.approx(before)

    def test_exact_balance_withdrawal_succeeds(self, ctx, customer_id):
        balance = get_balance(customer_id)
        success, _ = withdraw(customer_id, str(balance))
        assert success is True
        assert get_balance(customer_id) == pytest.approx(0.0)

    def test_zero_withdrawal_rejected(self, ctx, customer_id):
        success, _ = withdraw(customer_id, "0")
        assert success is False

    def test_non_numeric_withdrawal_rejected(self, ctx, customer_id):
        success, _ = withdraw(customer_id, "xyz")
        assert success is False


# ---------------------------------------------------------------------------
# Get balance tests
# ---------------------------------------------------------------------------

class TestGetBalance:

    def test_returns_correct_balance(self, ctx, customer_id):
        assert get_balance(customer_id) == pytest.approx(1000.0)

    def test_unknown_customer_returns_zero(self, ctx):
        assert get_balance(99999) == pytest.approx(0.0)
