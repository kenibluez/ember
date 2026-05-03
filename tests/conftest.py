import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base

@pytest.fixture
def session():
    """Provides a clean, in-memory database session for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    yield db_session
    db_session.close()

@pytest.fixture
def task_service(session):
    from app.services.task_service import TaskService
    return TaskService(session)
