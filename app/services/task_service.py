from sqlalchemy.orm import Session
from app.core.repositories.task_repository import TaskRepository
from app.core.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.core.models.task import Task, TaskStatus

class TaskService:
    """
    Service layer for Task operations, providing business logic and data transformation.
    Utilizes TaskRepository for database interactions.
    """
    def __init__(self, session: Session) -> None:
        self.repo = TaskRepository(session)

    def get_all(self) -> list[TaskRead]:
        """Retrieve all tasks and convert them to TaskRead schema."""
        tasks = self.repo.get_all()
        return [TaskRead.model_validate(task) for task in tasks]
    
    def create(self, data: TaskCreate) -> TaskRead:
        """Create a new task from TaskCreate schema and return it as TaskRead."""
        task = Task(**data.model_dump())
        created_task = self.repo.create(task)
        return TaskRead.model_validate(created_task)

    def update(self, id: int, data: TaskUpdate) -> TaskRead:
        """Update an existing task by ID with TaskUpdate schema and return it as TaskRead."""
        task = self.repo.get(id)
        if not task: 
            return None  # or raise an exception
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        self.repo.session.commit()
        self.repo.session.refresh(task)
        return TaskRead.model_validate(task)
    
    def mark_as(self, id: int, status: TaskStatus) -> TaskRead:
        """Convenience method to update only the status of a task."""
        return self.update(id, TaskUpdate(status=status))
