from werkzeug.security import check_password_hash
from models import Customer


def authenticate(username: str, password: str):
    """
    Verify credentials and return (success: bool, customer | None, message: str).

    The function deliberately returns the same generic error message for both
    "username not found" and "wrong password" to avoid leaking information.
    """
    if not username or not username.strip():
        return False, None, "Invalid username or password."

    if not password:
        return False, None, "Invalid username or password."

    customer = Customer.query.filter_by(username=username.strip()).first()

    if customer is None:
        return False, None, "Invalid username or password."

    if not check_password_hash(customer.password_hash, password):
        return False, None, "Invalid username or password."

    return True, customer, "Login successful."
