"""
Database setup for FastAPI.
Provides the SQLAlchemy engine, session factory, and a FastAPI dependency
that yields a database session per request and closes it when done.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./movie_explorer.db")

# SQLite needs connect_args for thread safety; ignored for other DBs
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency that provides a database session.
    Automatically closes the session when the request is done.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
