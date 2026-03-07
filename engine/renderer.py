import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from .dom_tree import ElementNode, TextNode

class DOMRenderer:
    """
    Takes our custom DOM Tree and draws it onto a blank PyQt Canvas.
    If a contributor wants to add full CSS support, they start here!
    """
    def __init__(self, engine_core):
        self.logger = logging.getLogger("PyWebCore.Engine.Renderer")
        self.engine_core = engine_core

    def render(self, dom_root):
        self.logger.info("Rendering DOM Tree to screen...")
        
        # Create a blank canvas for the page
        canvas = QWidget()
        layout = QVBoxLayout(canvas)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Give the page some realistic web-like margins
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(10)
        
        self._walk_tree(dom_root, layout)
        return canvas

    def _walk_tree(self, node, layout):
        for child in node.children:
            if isinstance(child, TextNode):
                pass # We extract text directly inside the element creator
                
            elif isinstance(child, ElementNode):
                widget = self._create_widget_for_element(child)
                if widget:
                    layout.addWidget(widget)
                
                # Recurse deeper (e.g., go inside <html>, <body>, <div>)
                self._walk_tree(child, layout)

    def _create_widget_for_element(self, element):
        """Maps HTML tags to primitive graphical widgets."""
        
        # Extract direct text children
        text_content = " ".join([c.text for c in element.children if isinstance(c, TextNode)])

        if element.tag == "h1":
            lbl = QLabel(text_content)
            lbl.setStyleSheet("font-size: 28px; font-weight: bold; color: #000000; margin-bottom: 10px;")
            return lbl
            
        elif element.tag in ["h2", "h3"]:
            lbl = QLabel(text_content)
            lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #222222; margin-bottom: 8px;")
            return lbl

        elif element.tag == "p":
            lbl = QLabel(text_content)
            lbl.setStyleSheet("font-size: 15px; color: #333333; line-height: 1.5;")
            lbl.setWordWrap(True)
            return lbl

        elif element.tag == "button":
            btn = QPushButton(text_content)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 8px 16px; 
                    font-size: 14px; 
                    background-color: #0d6efd; 
                    color: white; 
                    border-radius: 4px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # Hacky educational javascript execution!
            onclick = element.attributes.get("onclick", "")
            if "window.history.back()" in onclick:
                btn.clicked.connect(self.engine_core.go_back)
            elif "window.location.href" in onclick:
                # Extract URL from string like: window.location.href='test1.html'
                url = onclick.split("'")[1] if "'" in onclick else onclick.split('"')[1]
                btn.clicked.connect(lambda checked, u=url: self.engine_core.navigate(u))
            
            return btn
            
        elif element.tag == "li":
            lbl = QLabel(f"• {text_content}")
            lbl.setStyleSheet("font-size: 15px; color: #333333; margin-left: 20px;")
            return lbl
            
        # If it's a container like <html>, <body>, or <div>, we return None 
        # so _walk_tree can just look inside it for the real elements!
        return None
