from PySide6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

from app.components.view_switcher import ViewSwitcher
from app.viewmodels.calendar_vm import CalendarViewModel
from app.views.calendar.month_view import MonthView


class CalendarView(QWidget):
    def __init__(self, vm: CalendarViewModel, parent=None) -> None:
        super().__init__(parent)
        self.vm = vm
        self._setup_ui()

        self.vm.events_updated.connect(self._on_events_updated)
        self.vm.load_events()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # Switcher
        self.switcher = ViewSwitcher(["month", "week", "day", "year"])
        self.switcher.view_changed.connect(self._on_mode_switched)
        layout.addWidget(self.switcher)

        # Stack
        self.stack = QStackedWidget()
        self.month_view = MonthView()

        # Placeholders for the other views (to be built similarly to MonthView)
        # self.week_view = WeekView()
        # self.day_view = DayView()
        # self.year_view = YearView()

        self.stack.addWidget(self.month_view)
        layout.addWidget(self.stack)

    def _on_mode_switched(self, mode: str) -> None:
        # Extend mapping as other views are added
        mapping = {"month": 0, "week": 1, "day": 2, "year": 3}
        self.stack.setCurrentIndex(mapping.get(mode, 0))

    def _on_events_updated(self, events: list) -> None:
        self.month_view.update_events(events)
