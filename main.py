import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QStyle
from app.views.main_window import MainWindow

from app.styles.theme import Colors

def load_stylesheet(app: QApplication) -> None:
    qss_path = Path(__file__).parent / "app" / "styles" / "ember.qss"
    if qss_path.exists():
        with open(qss_path, "r") as f:
            content = f.read()
            # Format QSS with theme colors
            try:
                formatted_qss = content.format(**Colors.__dict__)
                app.setStyleSheet(formatted_qss)
            except KeyError as e:
                print(f"Error: Style variable {e} not found in theme.py")
                app.setStyleSheet(content)

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
