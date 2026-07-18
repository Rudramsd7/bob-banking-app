"""
Unit tests for services/auth_service.py

Run from BACKEND/ with:  python -m pytest tests/ -v
"""

import sys
import os

# Ensure BACKEND/ is on the path so imports resolve
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from flask import Flask
from werkzeug.security import generate_password_hash

from models import db, Customer
from services.auth_service import authenticate


@pytest.fixture
def app():
    """Create a throwaway Flask app backed by an in-memory SQLite database."""
    test_app = Flask(__name__)
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    test_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    test_app.config["SECRET_KEY"] = "test-secret"
    test_app.config["TESTING"] = True

    db.init_app(test_app)

    with test_app.app_context():
        db.create_all()
        # Seed a known test customer
        customer = Customer(
            username="testuser",
            password_hash=generate_password_hash("correct_password"),
            name="Test User",
            balance=500.0,
        )
        db.session.add(customer)
        db.session.commit()

        yield test_app

        db.drop_all()


@pytest.fixture
def ctx(app):
    """Push an application context for each test."""
    with app.app_context():
        yield


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestAuthenticate:

    def test_correct_credentials_return_success(self, ctx):
        success, customer, message = authenticate("testuser", "correct_password")
        assert success is True
        assert customer is not None
        assert customer.username == "testuser"

    def test_wrong_password_returns_failure(self, ctx):
        success, customer, message = authenticate("testuser", "wrong_password")
        assert success is False
        assert customer is None
        assert "Invalid" in message

    def test_nonexistent_username_returns_failure(self, ctx):
        success, customer, message = authenticate("nobody", "correct_password")
        assert success is False
        assert customer is None

    def test_empty_username_returns_failure(self, ctx):
        success, customer, message = authenticate("", "correct_password")
        assert success is False
        assert customer is None

    def test_empty_password_returns_failure(self, ctx):
        success, customer, message = authenticate("testuser", "")
        assert success is False
        assert customer is None

    def test_whitespace_only_username_returns_failure(self, ctx):
        success, customer, message = authenticate("   ", "correct_password")
        assert success is False

    def test_error_message_is_generic(self, ctx):
        """Ensure the error message doesn't reveal whether the username exists."""
        _, _, msg_bad_user = authenticate("nobody", "pass")
        _, _, msg_bad_pass = authenticate("testuser", "wrong")
        assert msg_bad_user == msg_bad_pass
