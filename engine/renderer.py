import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from .dom_tree import ElementNode, TextNode

class DOMRenderer:
    """
    Takes our custom DOM Tree and draws it onto a blank PyQt Canvas.
    Now equipped with generic tag fallbacks and hyperlink support!
    """
    def __init__(self, engine_core):
        self.logger = logging.getLogger("PyWebCore.Engine.Renderer")
        self.engine_core = engine_core

    def render(self, dom_root):
        self.logger.info("Rendering DOM Tree to screen...")
        
        canvas = QWidget()
        layout = QVBoxLayout(canvas)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(10)
        
        self._walk_tree(dom_root, layout)
        return canvas

    def _walk_tree(self, node, layout):
        for child in node.children:
            if isinstance(child, TextNode):
                pass 
                
            elif isinstance(child, ElementNode):
                # We skip script and style tags completely so their raw code doesn't print to the screen!
                if child.tag in ["script", "style", "noscript", "meta"]:
                    continue

                widget = self._create_widget_for_element(child)
                if widget:
                    layout.addWidget(widget)
                
                # Recurse deeper into nested elements
                self._walk_tree(child, layout)

    def _create_widget_for_element(self, element):
        """Maps HTML tags to primitive graphical widgets."""
        
        # Extract direct text children
        text_content = " ".join([c.text for c in element.children if isinstance(c, TextNode)]).strip()

        # 1. Hyperlinks (<a> tags)
        if element.tag == "a":
            if not text_content:
                return None
                
            btn = QPushButton(text_content)
            btn.setStyleSheet("""
                QPushButton {
                    color: #1a0dab; 
                    text-decoration: underline; 
                    border: none; 
                    background: transparent;
                    text-align: left;
                    font-size: 15px;
                }
                QPushButton:hover {
                    color: #d93025;
                }
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
            href = element.attributes.get("href", "")
            if href:
                # When clicked, tell the engine to navigate to the link!
                btn.clicked.connect(lambda checked, url=href: self.engine_core.navigate(url))
            return btn

        # 2. Headings
        elif element.tag == "h1":
            lbl = QLabel(text_content)
            lbl.setStyleSheet("font-size: 28px; font-weight: bold; color: #000000; margin-bottom: 10px;")
            lbl.setWordWrap(True)
            return lbl
            
        elif element.tag in ["h2", "h3", "h4", "h5", "h6"]:
            lbl = QLabel(text_content)
            lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #222222; margin-bottom: 8px;")
            lbl.setWordWrap(True)
            return lbl

        # 3. Paragraphs and Buttons
        elif element.tag == "p":
            if not text_content: return None
            lbl = QLabel(text_content)
            lbl.setStyleSheet("font-size: 15px; color: #333333; line-height: 1.5;")
            lbl.setWordWrap(True)
            return lbl

        elif element.tag == "button":
            btn = QPushButton(text_content)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 8px 16px; font-size: 14px; 
                    background-color: #0d6efd; color: white; 
                    border-radius: 4px; border: none;
                }
                QPushButton:hover { background-color: #0b5ed7; }
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
            onclick = element.attributes.get("onclick", "")
            if "window.history.back()" in onclick:
                btn.clicked.connect(self.engine_core.go_back)
            elif "window.location.href" in onclick:
                url = onclick.split("'")[1] if "'" in onclick else onclick.split('"')[1]
                btn.clicked.connect(lambda checked, u=url: self.engine_core.navigate(u))
            
            return btn
            
        elif element.tag == "li":
            if not text_content: return None
            lbl = QLabel(f"• {text_content}")
            lbl.setStyleSheet("font-size: 15px; color: #333333; margin-left: 20px;")
            lbl.setWordWrap(True)
            return lbl
            
        # 4. GENERIC FALLBACK (The Google Fix)
        # If it's a tag we don't know (span, b, div, etc.), but it has text directly inside it, 
        # print the text as a standard label so it isn't invisible!
        else:
            # We don't want to print text for structural root elements yet, just inline ones.
            if text_content and element.tag not in ["html", "body", "head", "document"]:
                lbl = QLabel(text_content)
                lbl.setStyleSheet("font-size: 15px; color: #555555;")
                lbl.setWordWrap(True)
                return lbl
            
        return None
