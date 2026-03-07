class DOMNode:
    """Base class for all nodes in our Document Object Model."""
    pass

class ElementNode(DOMNode):
    """An HTML Element (e.g., <h1>, <p>, <button>)."""
    def __init__(self, tag, attributes=None):
        self.tag = tag
        self.attributes = attributes or {}
        self.children = []

    def __repr__(self):
        return f"<Element {self.tag}>"

class TextNode(DOMNode):
    """Raw text inside an HTML element."""
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'"{self.text.strip()}"'
