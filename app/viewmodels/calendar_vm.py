from datetime import datetime, timedelta

from PySide6.QtCore import Signal

from app.services.calendar_service import CalendarService
from app.viewmodels.base_vm import BaseViewModel


class CalendarViewModel(BaseViewModel):
    events_updated = Signal(list)

    def __init__(self, service: CalendarService, parent=None) -> None:
        super().__init__(parent)
        self._service = service
        self._current_date = datetime.now()

    def load_events(self) -> None:
        """Loads events for a broad range (e.g., +/- 1 year from current date)"""
        self.loading_changed.emit(True)

        start = self._current_date - timedelta(days=365)
        end = self._current_date + timedelta(days=365)

        events = self._service.get_by_range(start, end)
        self.events_updated.emit(events)

        self.loading_changed.emit(False)
