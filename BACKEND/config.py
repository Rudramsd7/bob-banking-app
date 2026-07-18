import os

# Base directory of this file (BACKEND/)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key — used by Flask to sign session cookies.
# Change this to a long random value in any real deployment.
SECRET_KEY = "banking-workshop-secret-key-change-in-production-32bytes!"

# SQLite database file stored inside the BACKEND folder
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "bank.db")

# Disable SQLAlchemy event system overhead (not needed here)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Enable debug mode during development
DEBUG = True

# Maximum single-transaction amount (safeguard)
MAX_TRANSACTION_AMOUNT = 1_000_000
