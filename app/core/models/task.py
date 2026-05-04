# app/core/models/task.py

from sqlalchemy import String, Text, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC
from enum import Enum
from enum import StrEnum
from app.core.database import Base

class TaskStatus(StrEnum):
    """
    Enum representing the status of a task.
    """
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class TaskPriority(StrEnum):
    """
    Enum representing the priority of a task.
    """
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Task(Base):
    """SQLAlchemy model for the 'tasks' table."""
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
                                    SAEnum(TaskStatus), 
                                    default=TaskStatus.TODO, 
                                    nullable=False
                                )
    priority: Mapped[TaskPriority] = mapped_column(
                                        SAEnum(TaskPriority),
                                        default=TaskPriority.MEDIUM,
                                        nullable=False
                                    )
    due_date: Mapped[datetime] = mapped_column(
                                        DateTime, 
                                        nullable=True
                                )
    created_at: Mapped[datetime] = mapped_column(
                                        DateTime, 
                                        default=datetime.now(UTC), 
                                        nullable=False
                                    )
    updated_at: Mapped[datetime] = mapped_column(
                                        DateTime, 
                                        default=datetime.now(UTC),
                                        onupdate=datetime.now(UTC),
                                        nullable=False
                                    )