from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from services.auth_service import authenticate

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET"])
def login_page():
    """Render the login form. Redirect authenticated users to the dashboard."""
    if "customer_id" in session:
        return redirect(url_for("dashboard.dashboard_page"))
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login_submit():
    """Process login form submission."""
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    success, customer, message = authenticate(username, password)

    if success:
        session.clear()
        session["customer_id"] = customer.id
        session["customer_name"] = customer.name
        return redirect(url_for("dashboard.dashboard_page"))

    flash(message, "error")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """Terminate the user session and redirect to login."""
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("auth.login_page"))
