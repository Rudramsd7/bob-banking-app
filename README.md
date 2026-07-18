# SecureBank — Banking Web Application

A lightweight, browser-based banking application built with **Flask** and **Bootstrap 5**.  
Customers can log in, view their balance, and perform deposits and withdrawals.

---

## Project Structure

```
Banking_workshop/
├── BACKEND/
│   ├── app.py                    # Flask entry point
│   ├── config.py                 # All configuration (secret key, DB path)
│   ├── models.py                 # SQLAlchemy ORM models + DB seed
│   ├── requirements.txt          # Python dependencies
│   ├── routes/
│   │   ├── auth.py               # Login / logout routes
│   │   ├── dashboard.py          # Dashboard route
│   │   └── transactions.py       # Deposit / withdraw routes
│   ├── services/
│   │   ├── auth_service.py       # Credential verification logic
│   │   └── account_service.py    # Balance update & transaction logic
│   └── tests/
│       ├── test_auth_service.py  # Unit tests — authentication
│       ├── test_account_service.py # Unit tests — account operations
│       └── test_integration.py   # Integration tests — full request cycle
└── FRONTEND/
    ├── templates/
    │   ├── layout.html           # Base template (navbar, flash messages)
    │   ├── login.html            # Login page
    │   ├── dashboard.html        # Dashboard with deposit/withdraw forms
    │   └── errors/
    │       ├── 404.html
    │       └── 500.html
    └── static/
        ├── css/bootstrap.min.css
        └── js/bootstrap.bundle.min.js
```

---

## Prerequisites

- **Python 3.9+** — [python.org](https://python.org)
- A modern browser (Chrome, Firefox, Edge, Safari)

---

## Quick Start

### 1. Create and activate a virtual environment

```powershell
# Windows (PowerShell)
python -m venv BACKEND\venv
BACKEND\venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
python3 -m venv BACKEND/venv
source BACKEND/venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r BACKEND/requirements.txt
```

### 3. Run the application

```bash
python BACKEND/app.py
```

Flask will start and print:
```
 * Running on http://127.0.0.1:5000
```

Open **http://127.0.0.1:5000** in your browser.

### 4. Log in with the demo account

| Field    | Value         |
|----------|---------------|
| Username | `john_doe`    |
| Password | `password123` |

The demo customer starts with a **$1,000.00** balance.

---

## Running Tests

```bash
# From the project root
python -m pytest BACKEND/tests/ -v
```

All 38 tests should pass (unit + integration).

---

## Application Features

| Feature | Description |
|---|---|
| **Secure login** | Passwords stored as bcrypt hashes via Werkzeug |
| **Session management** | Server-signed Flask session cookies |
| **Dashboard** | Shows live balance and last 10 transactions |
| **Deposit** | Add funds; validated server-side and client-side |
| **Withdraw** | Deduct funds with overdraft protection |
| **Auth guards** | Every protected route checks the session |
| **Flash messages** | User feedback for every action |
| **Custom error pages** | 404 and 500 handlers |

---

## Security Notes

- Passwords are **never stored in plain text** — Werkzeug's `generate_password_hash` / `check_password_hash` are used.
- The session stores only `customer_id` and `customer_name` — the balance is always read fresh from the database.
- Error messages for failed logins are **generic** (no username/password distinction) to prevent user enumeration.
- All protected routes redirect unauthenticated requests to `/login`.
- The `SECRET_KEY` in `config.py` should be replaced with a long random value for any real deployment.

---

## Production Checklist (beyond this workshop)

- [ ] Set `DEBUG = False` and load `SECRET_KEY` from an environment variable
- [ ] Switch to Gunicorn (Linux/Mac) or Waitress (Windows) as the WSGI server
- [ ] Replace SQLite with PostgreSQL or MySQL for concurrent access
- [ ] Enable HTTPS via a reverse proxy (Nginx + Let's Encrypt)
- [ ] Add `PERMANENT_SESSION_LIFETIME` for session timeout

---

*SecureBank — Educational workshop application. Not for production use.*
