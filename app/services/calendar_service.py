from sqlalchemy.orm import Session
from app.core.repositories.event_repository import EventRepository
from app.core.models.event import Event
from app.core.schemas.event import EventCreate, EventRead, EventUpdate
from datetime import datetime, UTC

class CalendarService:
    """
    Service layer for Calendar operations, providing business logic and data transformation.
    Utilizes EventRepository for database interactions.
    """

    def __init__(self, session: Session) -> None:
        self.repo = EventRepository(session)

    def get_all(self) -> list[EventRead]:
        """Retrieve all events and convert them to EventRead schema."""
        events = self.repo.get_all()
        return [EventRead.model_validate(event) for event in events]

    def get_by_range(self, start: datetime, end: datetime) -> list[EventRead]:
        """Retrieve events that fall within a specific time range."""
        events = self.repo.get_by_range(start, end)
        return [EventRead.model_validate(event) for event in events]

    def create(self, data: EventCreate) -> EventRead:
        event = Event(**data.model_dump())
        created = self.repo.create(event)
        return EventRead.model_validate(created)

    def update(self, id: int, data: EventUpdate) -> EventRead | None:
        event = self.repo.get(id)
        if not event:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(event, field, value)
        self.repo.session.commit()
        self.repo.session.refresh(event)
        return EventRead.model_validate(event)

    def delete(self, id: int) -> bool:
        return self.repo.delete(id)
