# app/core/repositories/base_respository.py

from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type

ModelT = TypeVar("ModelT")

class BaseRepository(Generic[ModelT]):
    """
    Generic repository providing basic CRUD operations.
    All specific repositories (Task, Event) will inherit from this.
    """
    def __init__(self, model: Type[ModelT], session: Session) -> None:
        self.model = model
        self.session = session
    
    def get(self, id: int) -> ModelT | None:
        "Fetch a single record by its primary key."
        return self.session.get(self.model, id)

    def get_all(self) -> list[ModelT]:
        """Fetch all records for this model."""
        return self.session.query(self.model).all()
    
    def create(self, obj: ModelT) -> ModelT:
        """Persist a new model instance to the database."""
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
    
    def delete(self, id: int) -> None:
        """Remove a record by ID. Returns True if succesfull"""
        obj = self.get(id)
        if not obj:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True