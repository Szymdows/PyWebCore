import os
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QIcon, QAction

class NavigationBar(QToolBar):
    """Handles only the top toolbar buttons (Back, Forward, Reload)."""
    
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
