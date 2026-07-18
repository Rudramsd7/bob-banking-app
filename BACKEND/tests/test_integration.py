"""
Integration tests — tests the full Flask request/response cycle using
Flask's built-in test client.

Run from BACKEND/ with:  python -m pytest tests/ -v
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from werkzeug.security import generate_password_hash

os.environ["TESTING"] = "1"

from models import db, Customer


BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.abspath(os.path.join(BACKEND_DIR, "..", "FRONTEND"))


@pytest.fixture(scope="module")
def app():
    """Build a Flask test app with an in-memory database."""
    from flask import Flask
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.transactions import transactions_bp

    test_app = Flask(
        __name__,
        template_folder=os.path.join(FRONTEND_DIR, "templates"),
        static_folder=os.path.join(FRONTEND_DIR, "static"),
    )
    test_app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY="integration-test-secret",
        TESTING=True,
        WTF_CSRF_ENABLED=False,
    )

    db.init_app(test_app)

    test_app.register_blueprint(auth_bp)
    test_app.register_blueprint(dashboard_bp)
    test_app.register_blueprint(transactions_bp)

    with test_app.app_context():
        db.create_all()
        _seed(test_app)

    yield test_app

    with test_app.app_context():
        db.drop_all()


def _seed(app_instance):
    with app_instance.app_context():
        if Customer.query.count() == 0:
            c = Customer(
                username="int_user",
                password_hash=generate_password_hash("int_pass"),
                name="Integration User",
                balance=500.0,
            )
            db.session.add(c)
            db.session.commit()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_balance(app):
    """Reset the test customer's balance before each test."""
    with app.app_context():
        customer = Customer.query.filter_by(username="int_user").first()
        customer.balance = 500.0
        db.session.commit()


class TestAuthRoutes:

    def test_login_page_loads(self, client):
        response = client.get("/login")
        assert response.status_code == 200
        assert b"Sign In" in response.data

    def test_correct_login_redirects_to_dashboard(self, client):
        response = client.post(
            "/login",
            data={"username": "int_user", "password": "int_pass"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "/dashboard" in response.headers["Location"]

    def test_wrong_password_returns_login_page_with_error(self, client):
        response = client.post(
            "/login",
            data={"username": "int_user", "password": "wrong"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Invalid" in response.data

    def test_nonexistent_user_returns_generic_error(self, client):
        response = client.post(
            "/login",
            data={"username": "ghost", "password": "pass"},
            follow_redirects=True,
        )
        assert b"Invalid" in response.data

    def test_logout_clears_session(self, client):
        client.post("/login", data={"username": "int_user", "password": "int_pass"})
        response = client.get("/logout", follow_redirects=True)
        assert b"Sign In" in response.data


class TestAuthGuard:

    def test_dashboard_without_session_redirects_to_login(self, client):
        response = client.get("/dashboard", follow_redirects=False)
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]

    def test_deposit_without_session_redirects_to_login(self, client):
        response = client.post(
            "/deposit", data={"amount": "100"}, follow_redirects=False
        )
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]

    def test_withdraw_without_session_redirects_to_login(self, client):
        response = client.post(
            "/withdraw", data={"amount": "50"}, follow_redirects=False
        )
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]


class TestTransactionRoutes:

    @pytest.fixture(autouse=True)
    def logged_in_client(self, client):
        client.post("/login", data={"username": "int_user", "password": "int_pass"})
        return client

    def test_valid_deposit_increases_balance(self, client, app):
        client.post("/deposit", data={"amount": "200.00"})
        with app.app_context():
            customer = Customer.query.filter_by(username="int_user").first()
            assert customer.balance == pytest.approx(700.0)

    def test_deposit_shows_success_message(self, client):
        response = client.post(
            "/deposit", data={"amount": "100"}, follow_redirects=True
        )
        assert b"deposited" in response.data.lower()

    def test_valid_withdrawal_decreases_balance(self, client, app):
        client.post("/withdraw", data={"amount": "100.00"})
        with app.app_context():
            customer = Customer.query.filter_by(username="int_user").first()
            assert customer.balance == pytest.approx(400.0)

    def test_overdraft_rejected_with_error_message(self, client):
        response = client.post(
            "/withdraw", data={"amount": "9999"}, follow_redirects=True
        )
        assert b"Insufficient" in response.data

    def test_overdraft_does_not_change_balance(self, client, app):
        client.post("/withdraw", data={"amount": "9999"})
        with app.app_context():
            customer = Customer.query.filter_by(username="int_user").first()
            assert customer.balance == pytest.approx(500.0)

    def test_zero_deposit_rejected(self, client):
        response = client.post(
            "/deposit", data={"amount": "0"}, follow_redirects=True
        )
        assert b"greater than zero" in response.data.lower()

    def test_non_numeric_amount_rejected(self, client):
        response = client.post(
            "/deposit", data={"amount": "abc"}, follow_redirects=True
        )
        assert b"valid" in response.data.lower()
