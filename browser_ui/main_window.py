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
        
        # Connect the URL bar "Enter" key to the engine's navigate function
        self.nav_bar.url_bar.returnPressed.connect(self.on_url_bar_entered)

        # 3. Bind Engine Core output to our Web View display and URL bar
        self.engine.set_ui_callbacks(
            render_callback=self.web_view.display_rendered_page,
            url_callback=self.update_url_bar
        )

        # 4. Tell the engine to load the homepage!
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        homepage_path = os.path.join(base_dir, "homepage.html")
        self.engine.navigate(homepage_path)

    def on_url_bar_entered(self):
        """Triggered when the user presses Enter in the address bar."""
        url = self.nav_bar.url_bar.text().strip()
        if url:
            # Quick quality-of-life fix: auto-add http:// if they just type example.com
            if not url.startswith("http") and not url.endswith(".html"):
                url = "http://" + url
            self.engine.navigate(url)

    def update_url_bar(self, url):
        """Triggered by the engine when a page successfully loads."""
        self.nav_bar.url_bar.setText(url)
