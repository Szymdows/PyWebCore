import os
import logging
import urllib.request
from urllib.error import URLError
import ssl  # Added for SSL handling

from .html_parser import CustomHTMLParser
from .renderer import DOMRenderer

class WebEngineCore:
    def __init__(self):
        self.logger = logging.getLogger("PyWebCore.Engine")
        self.parser = CustomHTMLParser()
        self.renderer = DOMRenderer(self)
        
        self.history_back = []
        self.history_forward = []
        self.current_url = None
        self.current_dir = ""

        self.on_render_complete = None
        self.on_url_changed = None

    def set_ui_callbacks(self, render_callback, url_callback):
        self.on_render_complete = render_callback
        self.on_url_changed = url_callback

    def navigate(self, path, is_history_action=False):
        self.logger.info(f"Navigating to: {path}")
        html_string = ""

        if path.startswith("http://") or path.startswith("https://"):
            try:
                # Create an unverified SSL context to bypass certificate errors
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                req = urllib.request.Request(path, headers={'User-Agent': 'PyWebCore/1.0'})
                # Pass the SSL context into urlopen
                with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
                    html_string = response.read().decode('utf-8', errors='ignore')
                self.current_dir = "" 
            except URLError as e:
                self.logger.error(f"Failed to fetch URL: {e}")
                html_string = f"<html><body><h1>Network Error</h1><p>{e}</p></body></html>"
        else:
            if not os.path.isabs(path):
                path = os.path.normpath(os.path.join(self.current_dir, path))

            if not os.path.exists(path):
                self.logger.error("File not found!")
                html_string = "<html><body><h1>404 File Not Found</h1></body></html>"
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    html_string = f.read()
                self.current_dir = os.path.dirname(path)

        if self.current_url and not is_history_action:
            self.history_back.append(self.current_url)
            self.history_forward.clear()

        self.current_url = path

        if self.on_url_changed:
            self.on_url_changed(self.current_url)

        dom_tree = self.parser.parse_html(html_string)
        rendered_canvas = self.renderer.render(dom_tree)

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
