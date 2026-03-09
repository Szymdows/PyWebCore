import logging
from html.parser import HTMLParser as BaseHTMLParser
from .dom_tree import ElementNode, TextNode

# HTML5 void elements that never have closing tags!
VOID_ELEMENTS = ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"]

class CustomHTMLParser(BaseHTMLParser):
    """
    Educational HTML Parser. 
    Reads raw HTML strings and builds our custom DOM Tree.
    """
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("PyWebCore.Engine.HTMLParser")
        self.root = ElementNode("document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = ElementNode(tag, dict(attrs))
        
        # Always add the node as a child of whatever is currently on top of the stack
        self.stack[-1].children.append(node)

        # ONLY push to the stack if it is NOT a void element!
        # If it's a void element like <meta> or <img>, it can't have children.
        if tag not in VOID_ELEMENTS:
            self.stack.append(node)

    def handle_endtag(self, tag):
        # A real browser does complex tree reconstruction here. 
        # We will just pop elements off the stack until we find the matching tag.
        # This prevents poorly unclosed tags (like a missing </div>) from breaking the whole page!
        for i in reversed(range(len(self.stack))):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]  # Pop everything up to this tag
                break

    def handle_data(self, data):
        text = data.strip()
        if text:
            # Don't add text content if we are inside a script or style tag
            if self.stack[-1].tag not in ["style", "script", "noscript", "title"]:
                self.stack[-1].children.append(TextNode(text))

    def parse_html(self, html_string):
        self.logger.info("Building custom DOM Tree from HTML...")
        self.root = ElementNode("document")
        self.stack = [self.root]
        
        try:
            self.feed(html_string)
        except Exception as e:
            self.logger.error(f"Minor parsing error (ignoring): {e}")
            
        return self.root
