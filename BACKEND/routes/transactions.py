from flask import Blueprint, request, redirect, url_for, session, flash

from services.account_service import deposit, withdraw, get_balance

transactions_bp = Blueprint("transactions", __name__)


def _require_login():
    """Return a redirect if the user is not authenticated, else None."""
    if "customer_id" not in session:
        return redirect(url_for("auth.login_page"))
    return None


@transactions_bp.route("/deposit", methods=["POST"])
def deposit_funds():
    """Accept a deposit form submission and update the customer's balance."""
    guard = _require_login()
    if guard:
        return guard

    customer_id = session["customer_id"]
    raw_amount = request.form.get("amount", "")

    success, message = deposit(customer_id, raw_amount)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("dashboard.dashboard_page"))


@transactions_bp.route("/withdraw", methods=["POST"])
def withdraw_funds():
    """Accept a withdrawal form submission and update the customer's balance."""
    guard = _require_login()
    if guard:
        return guard

    customer_id = session["customer_id"]
    raw_amount = request.form.get("amount", "")

    if not raw_amount:
        flash("Amount is required", "error")
        return redirect(url_for("dashboard.dashboard_page"))

    if not float(raw_amount) > 0:
        flash("Amount must be greater than zero", "error")
        return redirect(url_for("dashboard.dashboard_page"))

    if float(raw_amount) > get_balance(customer_id):
        flash("Insufficient funds", "error")
        return redirect(url_for("dashboard.dashboard_page"))

    success, message = withdraw(customer_id, raw_amount)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("dashboard.dashboard_page"))
