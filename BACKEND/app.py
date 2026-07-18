import os
import sys

# Allow Python to find models, config etc. from the BACKEND directory
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, render_template

import config
from models import db, init_db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.transactions import transactions_bp

# ---------------------------------------------------------------------------
# Resolve paths relative to this file so the app works from any working dir
# ---------------------------------------------------------------------------
BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BACKEND_DIR, "..", "FRONTEND"))

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, "templates"),
    static_folder=os.path.join(FRONTEND_DIR, "static"),
)

# ---------------------------------------------------------------------------
# Load configuration
# ---------------------------------------------------------------------------
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["DEBUG"] = config.DEBUG

# ---------------------------------------------------------------------------
# Initialise database ORM
# ---------------------------------------------------------------------------
db.init_app(app)

# ---------------------------------------------------------------------------
# Register blueprints
# ---------------------------------------------------------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(transactions_bp)

# ---------------------------------------------------------------------------
# Seed database on first run
# ---------------------------------------------------------------------------
init_db(app)

# ---------------------------------------------------------------------------
# Custom error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Server Error: {e}", exc_info=True)
    return render_template("errors/500.html"), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=config.DEBUG, host="127.0.0.1", port=5000)
