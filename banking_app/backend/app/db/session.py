# ─────────────────────────────────────────────────────────────
#  app/db/session.py
#  Person 3 owns this file. Write this FIRST — everyone needs it.
#  Provides: engine, SessionLocal, get_db()
# ─────────────────────────────────────────────────────────────

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Read DATABASE_URL from .env — falls back to SQLite in project root
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# check_same_thread=False is required for SQLite when used with FastAPI
# (multiple threads handle requests). Safe here because SQLAlchemy
# manages its own connection pool and session lifecycle.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False,  # set to True temporarily if you want to see raw SQL in the console
)

# Session factory — autocommit and autoflush are OFF so we control transactions explicitly
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency. Yields a DB session and guarantees it is closed
    after the request finishes, even if an exception is raised.

    Usage in a router:
        from app.db.session import get_db
        from sqlalchemy.orm import Session
        from fastapi import Depends

        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()