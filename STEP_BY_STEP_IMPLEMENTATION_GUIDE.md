# Banking Web Application — Step-by-Step Implementation Guide

> **Document Type:** Implementation Instructions (Plain English)  
> **Refers to:** IMPLEMENTATION_PLAN.md  
> **Version:** 1.0  
> **Status:** Ready for Development

---

## How to Use This Guide

This guide walks you through building the Banking Web Application phase by phase. Each section explains **what to do** and **why**, without writing the actual code for you. Follow the phases in order — each one depends on the previous being complete.

---

## Phase 1 — Environment Setup

### Step 1.1 — Verify Python is Installed

Before anything else, confirm Python 3.9 or higher is available on your machine.

### Step 1.2 — Create the Project Folder Structure

Create `Banking_workshop/` with `BACKEND/` and `FRONTEND/` subdirectories.

### Step 1.3 — Create and Activate a Virtual Environment

Inside `BACKEND/`, run `python -m venv venv` then activate it.

### Step 1.4 — Install Dependencies

```bash
pip install -r BACKEND/requirements.txt
```

---

## Phase 2 — Backend Implementation

See `IMPLEMENTATION_PLAN.md` for full component design details.

Key files to create:
- `BACKEND/config.py` — secret key, DB URI, debug flag
- `BACKEND/models.py` — Customer + Transaction ORM models
- `BACKEND/app.py` — Flask factory, blueprint registration, error handlers
- `BACKEND/routes/auth.py` — login/logout blueprints
- `BACKEND/routes/dashboard.py` — dashboard with auth guard
- `BACKEND/routes/transactions.py` — deposit/withdraw routes
- `BACKEND/services/auth_service.py` — credential verification
- `BACKEND/services/account_service.py` — balance update logic

---

## Phase 3 — Frontend Implementation

- `FRONTEND/templates/layout.html` — base template with navbar and flash messages
- `FRONTEND/templates/login.html` — login form
- `FRONTEND/templates/dashboard.html` — balance display + deposit/withdraw forms
- `FRONTEND/templates/errors/404.html` and `500.html`

---

## Phase 4 — Testing

```bash
python -m pytest BACKEND/tests/ -v
```

Unit tests cover `auth_service` and `account_service`. Integration tests cover the full request cycle via Flask test client.

---

*End of Step-by-Step Implementation Guide*
