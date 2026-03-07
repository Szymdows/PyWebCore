import os
import logging
from .html_parser import CustomHTMLParser
from .renderer import DOMRenderer

class WebEngineCore:
    """
    The main coordinator for our custom engine.
    Handles internal history, networking/file loading, parsing, and rendering.
    """
    def __init__(self):
        self.logger = logging.getLogger("PyWebCore.Engine")
        self.parser = CustomHTMLParser()
        self.renderer = DOMRenderer(self)
        
        # Browser History Stacks
        self.history_back = []
        self.history_forward = []
        self.current_url = None
        self.current_dir = ""

        # Callback to update the UI
        self.on_render_complete = None

    def set_ui_callback(self, callback):
        self.on_render_complete = callback

    def navigate(self, path, is_history_action=False):
        """Loads a file, parses it, renders it, and updates UI."""
        
        # Calculate absolute path based on current directory
        if not os.path.isabs(path):
            path = os.path.normpath(os.path.join(self.current_dir, path))

        self.logger.info(f"Navigating to: {path}")

        if not os.path.exists(path):
            self.logger.error("File not found!")
            return

        # History Management
        if self.current_url and not is_history_action:
            self.history_back.append(self.current_url)
            self.history_forward.clear()

        self.current_url = path
        self.current_dir = os.path.dirname(path)

        # 1. Fetch
        with open(path, 'r', encoding='utf-8') as f:
            html_string = f.read()

        # 2. Parse (Generate DOM)
        dom_tree = self.parser.parse_html(html_string)

        # 3. Render (Generate Visual Canvas)
        rendered_canvas = self.renderer.render(dom_tree)

        # 4. Paint to UI
        if self.on_render_complete:
            self.on_render_complete(rendered_canvas)

    def go_back(self):
        if self.history_back:
            self.history_forward.append(self.current_url)
            prev_url = self.history_back.pop()
            self.navigate(prev_url, is_history_action=True)

    def go_forward(self):
        if self.history_forward:
            self.history_back.append(self.current_url)
            next_url = self.history_forward.pop()
            self.navigate(next_url, is_history_action=True)

    def reload(self):
        if self.current_url:
            self.navigate(self.current_url, is_history_action=True)
