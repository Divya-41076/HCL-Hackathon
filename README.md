# NexaBank — AI-Powered Online Banking System

> Secure, intelligent digital banking platform built for HCL Hackathon
> **FastAPI · SQLAlchemy · SQLite · Streamlit · Groq AI**

---

## Overview

NexaBank is a full-stack digital banking system that enables customers to:

- Manage multiple bank accounts
- Perform secure fund transfers
- Raise and track service requests
- Get AI-powered insights into spending behavior

All without visiting a physical branch.

---

## Key Highlights

- **Secure Authentication** — JWT-based login with bcrypt password hashing
- **Atomic Transactions** — No partial transfers, full rollback on failure
- **AI Financial Insights** — Smart spending analysis using Groq (Llama 3.3 70B)
- **Clean Architecture** — Router → Service → Repository → ORM → DB
- **Real Banking Logic** — Not just CRUD, includes 5-rule transfer validation

---

## Features

### Customer Onboarding
- Register a new customer account with name, email, phone, and address
- Secure login with JWT token authentication
- Password hashing with bcrypt — plaintext passwords never stored

### Account Management
- Open multiple accounts per customer (SAVINGS or CURRENT)
- View account details, current balance, and account status
- Account status management — ACTIVE, FROZEN, CLOSED

### Fund Transfers
- Transfer funds between any two accounts instantly
- 5-rule business validation before every transfer
- Atomic debit + credit — if one fails, both roll back
- Full transaction record created on every successful transfer
- Insufficient balance and inactive account protection built in

### Transaction History
- View complete transaction history per account
- Displays sender, receiver, amount, status, and IST timestamp
- Outgoing and incoming transfers clearly distinguished

### Service Requests
- Raise support requests — card issue, statement, cheque book
- Track request status — OPEN, IN_PROGRESS, RESOLVED
- View all requests raised by the logged-in customer
- Staff can update request status via API

### AI Spending Insights
- One-click AI analysis powered by Groq + Llama 3.3 70B
- Analyzes last 10 transactions and current balance
- Returns a plain-English personalised financial insight in under 1 second
- Helps customers understand spending patterns without manual analysis

### Security
- JWT tokens for all protected routes
- bcrypt password hashing with truncation safety
- CORS middleware for frontend-backend communication
- Secrets managed via `.env` — never committed to Git

### Developer Experience
- Auto-generated Swagger UI at `/docs` — all APIs testable without frontend
- Clean layered architecture — easy to extend or swap any layer
- SQLite for zero-config setup — one line change to switch to PostgreSQL
- Streamlit frontend easily replaceable with React

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend API | FastAPI (Python) |
| Database | SQLite via SQLAlchemy ORM |
| Frontend | Streamlit |
| Authentication | JWT — python-jose + bcrypt |
| AI Insights | Groq API — Llama 3.3 70B |

---

## Project Structure

```
banking_app/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── requirements.txt
│   ├── seed.py                  # Demo data loader
│   └── app/
│       ├── core/
│       │   └── security.py      # JWT + password hashing
│       ├── db/
│       │   ├── base.py          # SQLAlchemy Base + model imports
│       │   └── session.py       # Engine + get_db dependency
│       ├── models/              # ORM models
│       │   ├── customer.py
│       │   ├── account.py
│       │   ├── transaction.py
│       │   ├── service_request.py
│       │   └── bank_staff.py
│       ├── schemas/             # Pydantic request/response schemas
│       ├── routers/             # FastAPI route handlers
│       │   ├── auth.py
│       │   ├── accounts.py
│       │   ├── transactions.py
│       │   ├── service_requests.py
│       │   └── insights.py
│       └── services/            # Business logic layer
│           ├── auth_service.py
│           ├── account_service.py
│           ├── transaction_service.py
│           ├── request_service.py
│           └── insights_service.py
└── frontend/
    ├── app.py                   # Streamlit entry point
    ├── utils/
    │   └── api_client.py        # All HTTP calls in one place
    └── pages/
        ├── login.py
        ├── dashboard.py
        ├── transfer.py
        ├── history.py
        ├── service_request.py
        └── insights.py
```

---

## Architecture

```
Streamlit UI → FastAPI Router → Service Layer → Repository → SQLAlchemy ORM → SQLite
```

Each layer has one responsibility:

- **Router** — HTTP routing + JWT authentication
- **Service** — all business rules and validation
- **Repository/ORM** — all database interaction
- **Schemas** — Pydantic request/response validation

---

## Database Schema

| Table | Description |
|-------|-------------|
| customers | User details and credentials |
| accounts | Bank accounts with balances |
| transactions | Fund transfer records |
| service_requests | Customer support requests |
| bank_staff | Admin and support staff |

**Relationships:**
- One customer → Many accounts (One-to-Many)
- One customer → Many service requests (One-to-Many)
- One account → Many transactions sent (One-to-Many)
- One account → Many transactions received (One-to-Many)

---

## Database Schema

![Database ERD](docs/erd.png)

| Table | Description |
|-------|-------------|
| customers | User details and credentials |
| accounts | Bank accounts with balances |
| transactions | Fund transfer records |
| service_requests | Customer support requests |
| bank_staff | Admin and support staff |

---

## API Endpoints

| Method | Route | Auth | Purpose |
|--------|-------|------|---------|
| POST | /auth/register | No | Register new customer |
| POST | /auth/login | No | Login — returns JWT token |
| GET | /auth/me | Yes | Get logged-in customer details |
| POST | /accounts/ | Yes | Create account (SAVINGS/CURRENT) |
| GET | /accounts/{id} | Yes | Get account details and balance |
| GET | /accounts/customer/{id} | Yes | List all accounts for customer |
| POST | /transactions/transfer | Yes | Atomic fund transfer |
| GET | /transactions/account/{id} | Yes | Transaction history |
| POST | /service-requests/ | Yes | Raise a service request |
| GET | /service-requests/{id} | Yes | Get request status |
| PUT | /service-requests/{id}/status | Yes | Update request status |
| GET | /service-requests/me | Yes | All requests for logged-in customer |
| GET | /insights/{account_id} | Yes | AI spending insights |

---

## Fund Transfer — 5 Business Rules

Every transfer enforces these rules in strict order:

1. Source account must exist → 404 if not
2. Destination account must exist → 404 if not
3. Both accounts must have `status = ACTIVE` → 403 if not
4. Source and destination must be different → 400 if same
5. Source balance must be >= transfer amount → 400 if insufficient

All rules pass → atomic `session.begin()` executes debit + credit together.
Any failure → full rollback. Both balances remain unchanged.

This guarantees **ACID compliance** — no partial or inconsistent state.

---

## AI Spending Insights

Uses **Groq + Llama 3.3 70B** to analyze the customer's last 10 transactions and current balance, returning a plain-English financial insight in under 1 second.

Example output:
> *"Your account balance is 9,500. You made 3 outgoing transfers totalling 2,000 this week. Consider reviewing recurring outflows to manage your balance better."*

---

## Setup and Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configure environment
Create `backend/.env`:
```env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at: https://console.groq.com

### Run backend
```bash
cd banking_app/backend
uvicorn main:app --reload
```

- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

### Run frontend
```bash
cd banking_app/frontend
streamlit run app.py
```

- UI: http://localhost:8501

---

## Demo Flow

1. Register a new customer → Login → JWT token issued
2. Create SAVINGS and CURRENT accounts
3. Transfer funds between accounts → balances update atomically
4. View transaction history with IST timestamps
5. Raise a service request → track status changes
6. Click AI Insights → Groq returns personalised spending analysis
7. Demo failed transfer (insufficient funds) → 400 error, both balances unchanged

---

## Notes

- SQLite used for zero-config hackathon demo — swap to PostgreSQL with one config line
- Streamlit can be replaced with React — zero backend changes required
- Service layer is fully decoupled from the transport layer
- All secrets must be in `.env` — never committed to Git

---

*NexaBank*
