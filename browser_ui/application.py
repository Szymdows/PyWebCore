import sys
from PyQt6.QtWidgets import QApplication

from engine.logger import configure_logging
from engine.core import WebEngineCore
from browser_ui.main_window import PyWebCoreWindow

def start_app():
    """Bootstraps and runs the entire PyWebCore application."""
    
    # 1. Start the logging subsystem
    configure_logging()
    
    # 2. Initialize the background engine logic
    engine = WebEngineCore()
    
    # 3. Create the Qt Application
    app = QApplication(sys.argv)
    
    # --- GLOBAL LIGHT THEME ---
    app.setStyleSheet("""
        QMainWindow, QScrollArea, QToolBar {
            background-color: #f8f9fa;
            color: #212529;
        }
        QToolBar {
            border-bottom: 1px solid #dee2e6;
            background-color: #ffffff;
        }
        QWidget {
            background-color: #ffffff;
            color: #000000;
        }
    """)
    
    # 4. Create UI and inject the engine
    window = PyWebCoreWindow(engine)
    window.show()
    
    # 5. Start the event loop
    sys.exit(app.exec())
