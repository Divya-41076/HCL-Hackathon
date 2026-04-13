# ─────────────────────────────────────────────────────────────
#  Online Banking Hackathon — main.py
#  Person 4 owns this file exclusively. Nobody else edits it.
#
#  Run with:
#    uvicorn main:app --reload --port 8000
#
#  Swagger UI available at: http://localhost:8000/docs
#  ReDoc available at:      http://localhost:8000/redoc
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# ── DB setup ──────────────────────────────────────────────────
from app.db.session import engine
from app.db.base import Base  # imports all models — must stay here

# ── Routers ───────────────────────────────────────────────────
from app.routers import auth, accounts, transactions, service_requests, insights


# ── Lifespan: create all tables on startup ────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs BEFORE the first request is handled.
    Creates all SQLAlchemy tables if they don't exist yet.
    Safe to call repeatedly — create_all is idempotent.
    """
    Base.metadata.create_all(bind=engine)
    print("✅  Database tables verified / created.")
    yield
    # Nothing to clean up on shutdown for SQLite


# ── App init ──────────────────────────────────────────────────
app = FastAPI(
    title="Online Banking API",
    description=(
        "3-Hour Hackathon · FastAPI + SQLAlchemy + SQLite\n\n"
        "All endpoints are documented below. "
        "Use POST /auth/register then POST /auth/login to get a Bearer token, "
        "then click Authorize (🔒) at the top right."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ── CORS — allow Streamlit frontend on any port ───────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten to ["http://localhost:8501"] post-demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Include all routers ───────────────────────────────────────
#  Each router registers its own prefix and tags.
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(service_requests.router)
app.include_router(insights.router)


# ── Health check — Person 4 uses this to confirm server is up ─
@app.get("/health", tags=["Health"])
def health_check():
    """
    Quick liveness check.
    GET http://localhost:8000/health → {"status": "ok"}
    Use this to confirm uvicorn is running before running the integration checklist.
    """
    return {"status": "ok", "message": "Online Banking API is running."}


# ── Dev entrypoint (optional — prefer uvicorn CLI) ────────────
# Uncomment only if running `python main.py` directly during dev:
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)