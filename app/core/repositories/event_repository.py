from sqlalchemy.orm import Session
from app.core.repositories.base_repository import BaseRepository
from app.core.models.event import Event

class EventRepository(BaseRepository[Event]):
    def __init__(self, session: Session) -> None:
        super().__init__(Event, session)
