import os
from PyQt6.QtWidgets import QMainWindow
from browser_ui.navigation_bar import NavigationBar
from browser_ui.web_view import CustomWebView

class PyWebCoreWindow(QMainWindow):
    """The main window that glues our UI and custom Engine together."""
    
    def __init__(self, engine):
        super().__init__()
        self.engine = engine 
        
        self.setWindowTitle("PyWebCore - Custom Educational Engine")
        self.resize(1024, 768)

        # 1. Initialize UI Components
        self.web_view = CustomWebView(self)
        self.nav_bar = NavigationBar(self)

        self.setCentralWidget(self.web_view)
        self.addToolBar(self.nav_bar)

        # 2. Bind UI buttons to Engine Core logic
        self.nav_bar.back_action.triggered.connect(self.engine.go_back)
        self.nav_bar.forward_action.triggered.connect(self.engine.go_forward)
        self.nav_bar.reload_action.triggered.connect(self.engine.reload)

        # 3. Bind Engine Core output to our Web View display
        self.engine.set_ui_callback(self.web_view.display_rendered_page)

        # 4. Tell the engine to load the homepage!
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        homepage_path = os.path.join(base_dir, "homepage.html")
        self.engine.navigate(homepage_path)
