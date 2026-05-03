# app/core/schemas/task.py

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.core.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title:       str
    description: str | None = None
    status:      TaskStatus = TaskStatus.TODO
    priority:    TaskPriority = TaskPriority.MEDIUM
    due_date:    datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: str | None = None  # all fields optional on update


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id:         int
    created_at: datetime
    updated_at: datetime