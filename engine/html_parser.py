import logging
from html.parser import HTMLParser as BaseHTMLParser
from .dom_tree import ElementNode, TextNode

class CustomHTMLParser(BaseHTMLParser):
    """
    Educational HTML Parser. 
    Reads raw HTML strings and builds our custom DOM Tree.
    Contributors can replace this with a from-scratch tokenizer later!
    """
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("PyWebCore.Engine.HTMLParser")
        self.root = ElementNode("document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        # Ignore head and style for our basic visual renderer
        if tag in ["head", "style", "meta", "title"]:
            self.stack.append(ElementNode(tag)) # Push but we might ignore rendering it
            return

        node = ElementNode(tag, dict(attrs))
        self.stack[-1].children.append(node)
        self.stack.append(node)

    def handle_endtag(self, tag):
        if len(self.stack) > 1:
            self.stack.pop()

    def handle_data(self, data):
        text = data.strip()
        if text:
            # Don't add text for style/script tags
            if self.stack[-1].tag not in ["style", "script", "head", "title"]:
                self.stack[-1].children.append(TextNode(text))

    def parse_html(self, html_string):
        self.logger.info("Building custom DOM Tree from HTML...")
        self.root = ElementNode("document")
        self.stack = [self.root]
        self.feed(html_string)
        return self.root
