# app/core/schemas/event.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    """Base fields for calendar events."""

    title: str
    description: str | None = None
    start_dt: datetime
    end_dt: datetime
    all_day: bool = False


class EventCreate(EventBase):
    """Schema for creating a new event. Inherits all fields from EventBase."""

    pass


class EventUpdate(EventBase):
    """Schema for updating an existing event. All fields are optional."""


class EventRead(EventBase):
    """Schema for reading an event from the database. Includes ID and timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
