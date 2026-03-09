import os
from PyQt6.QtWidgets import QToolBar, QLineEdit
from PyQt6.QtGui import QIcon, QAction

class NavigationBar(QToolBar):
    """Handles the top toolbar buttons and the URL address bar."""
    
    def __init__(self, parent=None):
        super().__init__("Navigation", parent)
        self.setMovable(False)
        
        # Resolve icon directory dynamically
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icons_dir = os.path.join(base_dir, "icons")

        # Create actions with SVGs
        self.back_action = QAction(QIcon(os.path.join(icons_dir, "back.svg")), "Back", self)
        self.forward_action = QAction(QIcon(os.path.join(icons_dir, "forward.svg")), "Forward", self)
        self.reload_action = QAction(QIcon(os.path.join(icons_dir, "reload.svg")), "Reload", self)

        # Add buttons to the toolbar
        self.addAction(self.back_action)
        self.addAction(self.forward_action)
        self.addAction(self.reload_action)

        # Add Address Bar (URL Input)
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or local path (e.g., http://example.com)")
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 12px;
                padding: 4px 10px;
                margin-left: 10px;
                margin-right: 10px;
                background-color: #f1f3f4;
            }
        """)
        self.addWidget(self.url_bar)
