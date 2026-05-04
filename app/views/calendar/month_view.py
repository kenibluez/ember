import calendar
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QWidget

from app.components.day_cell import DayCell


class MonthView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.lay = QGridLayout(self)
        self.lay.setSpacing(5)
        self.cells: dict[int, DayCell] = {}
        self._build_grid()

    def _build_grid(self) -> None:
        # Header Row (Days of Week)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days):
            lbl = QLabel(day)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setObjectName("calendar-header-label")
            self.lay.addWidget(lbl, 0, col)

        # Build the 6x7 grid for the current month
        now = datetime.now()
        cal = calendar.Calendar(firstweekday=0)  # Monday first
        month_days = cal.monthdayscalendar(now.year, now.month)

        for row, week in enumerate(month_days):
            for col, day in enumerate(week):
                cell = DayCell(day)
                if day != 0:
                    self.cells[day] = cell
                self.lay.addWidget(cell, row + 1, col)

    def update_events(self, events: list) -> None:
        now = datetime.now()
        for event in events:
            # Simple matching for current month events
            if event.start_dt.year == now.year and event.start_dt.month == now.month:
                day = event.start_dt.day
                if day in self.cells:
                    self.cells[day].add_event_dot(event.title)
