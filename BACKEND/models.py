from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


def _utcnow():
    """Return a timezone-naive UTC datetime (SQLite compatible)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)

db = SQLAlchemy()


class Customer(db.Model):
    """Represents a bank customer account."""

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

    # Relationship to transactions (one customer → many transactions)
    transactions = db.relationship(
        "Transaction", backref="customer", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Customer {self.username} balance={self.balance:.2f}>"


class Transaction(db.Model):
    """Records every deposit and withdrawal against a customer account."""

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customers.id"), nullable=False
    )
    transaction_type = db.Column(
        db.String(20), nullable=False
    )  # "deposit" | "withdrawal"
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=_utcnow)

    def __repr__(self):
        return (
            f"<Transaction {self.transaction_type} {self.amount:.2f} "
            f"@ {self.timestamp.strftime('%Y-%m-%d %H:%M')}>"
        )


def init_db(app):
    """Create all tables and seed a test customer if none exist."""
    with app.app_context():
        db.create_all()
        _seed_test_customer()


def _seed_test_customer():
    """Insert a default test customer if the table is empty."""
    if Customer.query.count() == 0:
        test_customer = Customer(
            username="john_doe",
            password_hash=generate_password_hash("password123"),
            name="John Doe",
            balance=1000.00,
        )
        db.session.add(test_customer)
        db.session.commit()
        print("[DB] Seeded test customer: username=john_doe / password=password123")
