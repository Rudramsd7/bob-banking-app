# Banking Web Application — Implementation Plan

> **Document Type:** High-Level Planning  
> **Version:** 1.0  
> **Status:** Draft

---

## 1. Solution Overview

### 1.1 Objective

Deliver a lightweight, browser-based banking application that allows registered customers to securely log in, view their account balance, and perform basic financial transactions (deposit and withdrawal) through a clean, responsive interface.

### 1.2 Scope

| In Scope | Out of Scope |
|---|---|
| Customer login / logout | User self-registration |
| View current account balance | Multi-account support |
| Deposit funds | Inter-account transfers |
| Withdraw funds | Loan or credit features |
| Session-protected dashboard | Admin / back-office portal |
| SQLite-backed persistence | External payment gateways |

### 1.3 Users

- **Authenticated Customer** — the sole user role. A pre-seeded bank customer who can log in and manage their own account.

### 1.4 Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-01 | The system shall authenticate a customer using a username and password. |
| FR-02 | An authenticated customer shall be presented with a dashboard showing their name and current balance. |
| FR-03 | A customer shall be able to deposit a positive monetary amount that is immediately reflected in their balance. |
| FR-04 | A customer shall be able to withdraw a positive monetary amount, provided sufficient funds exist. |
| FR-05 | The system shall prevent access to any protected page if the customer is not authenticated. |
| FR-06 | A customer shall be able to log out, terminating their session. |

### 1.5 Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-01 | **Security** — Passwords must be stored as hashed values; sessions must be server-managed. |
| NFR-02 | **Usability** — All pages must be responsive and render correctly on desktop and tablet viewports. |
| NFR-03 | **Performance** — Page responses should be served within 500 ms under normal load on localhost. |
| NFR-04 | **Maintainability** — Frontend and backend must be cleanly separated into distinct folders. |
| NFR-05 | **Portability** — The application must run on any OS with Python 3.9+ and a modern browser. |

### 1.6 Assumptions

- A single SQLite database file is sufficient for this workshop-scale application.
- Customer accounts are pre-seeded; no public registration flow is required.
- The application is deployed and tested locally (not production-hardened).
- Bootstrap is loaded from the project's static assets (no CDN dependency required at runtime).
- One session per customer; concurrent multi-device sessions are not in scope.

---

## 2. High-Level Architecture

### 2.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                        BROWSER                          │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │              FRONTEND  (FRONTEND/)               │   │
│  │   HTML Templates  +  Bootstrap CSS/JS            │   │
│  │   login.html  │  dashboard.html  │  layout.html  │   │
│  └───────────────────────┬──────────────────────────┘   │
└──────────────────────────│──────────────────────────────┘
                           │  HTTP Request (form POST / GET)
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   BACKEND  (BACKEND/)                   │
│                                                         │
│   ┌──────────────┐   ┌────────────┐   ┌─────────────┐  │
│   │  Flask App   │──▶│  Routes /  │──▶│  Business   │  │
│   │  (app.py)    │   │  Blueprints│   │  Logic      │  │
│   └──────────────┘   └────────────┘   └──────┬──────┘  │
│                                              │          │
│                                   ┌──────────▼───────┐  │
│                                   │  SQLite ORM /    │  │
│                                   │  DB Layer        │  │
│                                   └──────────┬───────┘  │
└──────────────────────────────────────────────│──────────┘
                                               │  SQL Queries
                                               ▼
                                  ┌────────────────────────┐
                                  │   DATABASE  (BACKEND/) │
                                  │   bank.db  (SQLite)    │
                                  └────────────────────────┘
```

### 2.2 Request Lifecycle

1. **Browser** submits an HTTP request (GET for page loads, POST for form actions).
2. **Flask Router** matches the URL to the appropriate route handler.
3. **Route Handler** validates the session; unauthenticated requests are redirected to `/login`.
4. **Business Logic Layer** processes the request (verify credentials, compute new balance, etc.).
5. **Database Layer** reads from or writes to `bank.db` via SQLite.
6. **Flask** renders the appropriate HTML template with context data.
7. **Browser** displays the rendered page to the customer.

---

## 3. Folder Structure

```
Banking_workshop/
│
├── FRONTEND/                        # All browser-facing assets
│   ├── templates/                   # Jinja2 HTML templates
│   │   ├── layout.html
│   │   ├── login.html
│   │   └── dashboard.html
│   └── static/
│       ├── css/bootstrap.min.css
│       └── js/bootstrap.bundle.min.js
│
├── BACKEND/                         # Server-side application
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── routes/
│   ├── services/
│   ├── tests/
│   └── requirements.txt
│
├── IMPLEMENTATION_PLAN.md
└── README.md
```

---

*End of Implementation Plan*
