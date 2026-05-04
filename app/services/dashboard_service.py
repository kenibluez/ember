from sqlalchemy.orm import Session
from app.core.models.task import TaskStatus
from app.core.repositories.task_repository import TaskRepository
from app.core.repositories.event_repository import EventRepository
from datetime import date

class DashboardService:
    def __init__(self, session: Session) -> None:
        self.task_repo  = TaskRepository(session)
        self.event_repo = EventRepository(session)

    def get_stats(self) -> dict:
        """Aggregates counts and statuses for the dashboard view."""
        tasks = self.task_repo.get_all()
        return {
            "total": len(tasks),
            "todo": sum(1 for t in tasks if t.status == TaskStatus.TODO),
            "in_progress": sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS),
            "completed": sum(1 for t in tasks if t.status == TaskStatus.COMPLETED),
            "cancelled": sum(1 for t in tasks if t.status == TaskStatus.CANCELLED),
            "due_today": sum(
                1 for t in tasks if t.due_date and t.due_date.date() == date.today()
            ),
        }
