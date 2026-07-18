from flask import Blueprint, render_template, redirect, url_for, session

from models import Customer, db
from services.account_service import get_recent_transactions

dashboard_bp = Blueprint("dashboard", __name__)


def _require_login():
    """Return a redirect if the user is not authenticated, else None."""
    if "customer_id" not in session:
        return redirect(url_for("auth.login_page"))
    return None


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
def dashboard_page():
    """Render the main account dashboard for authenticated customers."""
    guard = _require_login()
    if guard:
        return guard

    customer = db.session.get(Customer, session["customer_id"])
    if customer is None:
        # Session references a deleted customer — clear and redirect
        session.clear()
        return redirect(url_for("auth.login_page"))

    transactions = get_recent_transactions(customer.id, limit=10)

    return render_template(
        "dashboard.html",
        customer=customer,
        transactions=transactions,
    )
