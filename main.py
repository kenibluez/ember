import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QStyle
from app.views.main_window import MainWindow

def load_stylesheet(app: QApplication) -> None:
    qss_path = Path(__file__).parent / "app" / "styles" / "ember.qss"
    if qss_path.exists():
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Ember")

    # Load Styles
    load_stylesheet(app)

    # Setup Tray Icon
    tray = QSystemTrayIcon(app.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
    tray.setToolTip("Ember")
    tray.show()

    # Launch Window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
