from sqlalchemy.orm import Session
from app.core.repositories.base_repository import BaseRepository
from app.core.models.event import Event
from datetime import datetime

class EventRepository(BaseRepository[Event]):
    def __init__(self, session: Session) -> None:
        super().__init__(Event, session)

    def get_by_range(self, start: datetime, end: datetime) -> list[Event]:
        """Fetch events that fall within a specific time range."""
        return (
            self.session.query(Event)
            .filter(Event.start_dt < end)
            .filter(Event.end_dt > start)
            .all()
        )
