import sys
import re
from pathlib import Path
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QStyle
from app.views.main_window import MainWindow

from app.styles.theme import Colors

def load_stylesheet(app: QApplication) -> None:
    qss_path = Path(__file__).parent / "app" / "styles" / "ember.qss"
    if qss_path.exists():
        with open(qss_path, "r") as f:
            content = f.read()
            
            # Extract color constants from theme.py
            color_vars = {k: v for k, v in Colors.__dict__.items() if k.isupper()}
            
            # Use regex to find and replace {VARIABLE}
            # This avoids conflict with CSS braces like QWidget { ... }
            def replace_match(match):
                var_name = match.group(1)
                return color_vars.get(var_name, match.group(0))
            
            formatted_qss = re.sub(r"\{(\w+)\}", replace_match, content)
            app.setStyleSheet(formatted_qss)

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
