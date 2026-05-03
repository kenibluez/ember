# app/viewmodels/task_vm.py

from PySide6.QtCore import Signal
from app.viewmodels.base_vm import BaseViewModel
from app.services.task_service import TaskService
from app.core.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.core.models.task import TaskStatus


class TaskViewModel(BaseViewModel):
    tasks_changed = Signal(list)    # emits list[TaskRead]
    task_created  = Signal(object)  # emits TaskRead
    task_deleted  = Signal(int)     # emits task id

    def __init__(self, service: TaskService, parent=None) -> None:
        super().__init__(parent)
        self._service = service
        self._tasks: list[TaskRead] = []

    def load_tasks(self) -> None:
        self.loading_changed.emit(True)
        self._tasks = self._service.get_all()
        self.tasks_changed.emit(self._tasks)
        self.loading_changed.emit(False)

    def create_task(self, data: TaskCreate) -> None:
        task = self._service.create(data)
        self._tasks.append(task)
        self.task_created.emit(task)
        self.tasks_changed.emit(self._tasks)

    def delete_task(self, id: int) -> None:
        if self._service.delete(id):
            self._tasks = [t for t in self._tasks if t.id != id]
            self.task_deleted.emit(id)
            self.tasks_changed.emit(self._tasks)

    def update_status(self, id: int, status: TaskStatus) -> None:
        updated = self._service.mark_as(id, status)
        if updated:
            self._tasks = [updated if t.id == id else t for t in self._tasks]
            self.tasks_changed.emit(self._tasks)