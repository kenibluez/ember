# app/core/repositories/task_repository.py

from sqlalchemy.orm import Session
from app.core.repositories.base_repository import BaseRepository
from app.core.models.task import Task, TaskStatus

class TaskRepository(BaseRepository[Task]):
    """
    Task-specific repository for managing Task database operations.
    Inherits generic CRUD from BaseRepository.
    """
    def __init__(self, session: Session) -> None:
        super().__init__(Task, session)

    def get_by_status(self, status: TaskStatus) -> list[Task]:
        """Fetch all tasks matching a specific status (e.g., TODO, DONE)."""
        return (
            self.session.query(Task)
            .filter(Task.status == status)
            .all()
        )

    def get_due_soon(self, within_minutes: int = 30) -> list[Task]:
        """
        Find tasks that have a due date within the next X minutes and are not yet done.
        This supports the notification service logic.
        """
        from datetime import datetime, timedelta
        
        now = datetime.utcnow()
        threshold = now + timedelta(minutes=within_minutes)
        
        return (
            self.session.query(Task)
            .filter(Task.due_date.between(now, threshold))
            .filter(Task.status != TaskStatus.DONE)
            .all()
        )