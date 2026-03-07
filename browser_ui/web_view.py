from PyQt6.QtWidgets import QScrollArea, QWidget

class CustomWebView(QScrollArea):
    """
    Our custom visual viewport.
    Instead of an off-the-shelf web engine, this simply acts as a blank 
    scrolling window that receives the Canvas created by our Engine's Renderer.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        
        # Set a blank initial widget
        blank = QWidget()
        blank.setStyleSheet("background-color: white;")
        self.setWidget(blank)

    def display_rendered_page(self, canvas_widget):
        """Receives the completely rendered page from our engine and displays it."""
        canvas_widget.setStyleSheet("background-color: white;")
        self.setWidget(canvas_widget)
