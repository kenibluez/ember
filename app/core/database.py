# app/core/database.py

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "sqlite:///ember.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },  # Needed for SQLite to allow multi-threaded access
    echo=False,  # Set to True for SQL query logging
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    """Declarative base class for all SQLAlchemy models."""

    pass


def get_session() -> Generator[Session, None, None]:
    """
    Generator function to provide a database session.
    Ensures the session is closed after use.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    """
    Initializes the database by creating all tables.
    """
    Base.metadata.create_all(bind=engine)
