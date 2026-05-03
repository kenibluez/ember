from PySide6.QtWidgets import QSystemTrayIcon
from PySide6.QtCore import QTimer
from app.services.task_service import TaskService

class NotificationService:
    """Monitors upcoming tasks and triggers system tray alerts."""
    CHECK_INTERVAL_MS = 60_000

    def __init__(self, tray: QSystemTrayIcon, task_service: TaskService) -> None:
        self._tray         = tray
        self._task_service = task_service
        self._notified_ids: set[int] = set()

        self._timer = QTimer()
        self._timer.timeout.connect(self._check_due_tasks)
        self._timer.start(self.CHECK_INTERVAL_MS)

    def _check_due_tasks(self) -> None:
        """Query repository for tasks due within 30 minutes."""
        due_tasks = self._task_service.repo.get_due_soon(within_minutes=30)
        for task in due_tasks:
            if task.id not in self._notified_ids:
                self._notify(task.title)
                self._notified_ids.add(task.id)

    def _notify(self, title: str) -> None:
        self._tray.showMessage(
            "🔥 Ember",
            f'"{title}" is due soon. Still smoldering?',
            QSystemTrayIcon.MessageIcon.Information,
            4000,
        )
