# app/core/schemas/event.py

from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EventBase(BaseModel):
    """Base fields for calendar events."""
    title:       str
    description: str | None = None
    start_time:  datetime
    end_time:    datetime
    all_day:     bool = False

class EventCreate(EventBase):
    """Schema for creating a new event. Inherits all fields from EventBase."""
    pass

class EventUpdate(EventBase):
    """Schema for updating an existing event. All fields are optional."""
    title:       str | None = None
    description: str | None = None
    start_time:  datetime | None = None
    end_time:    datetime | None = None
    all_day:     bool | None = None

class EventRead(EventBase):
    """Schema for reading an event from the database. Includes ID and timestamps."""
    model_config = ConfigDict(from_attributes=True)

    id:         int
    created_at: datetime
