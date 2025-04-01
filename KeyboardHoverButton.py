from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QColor

class KeyboardHoverButton(QPushButton):
    """Custom button that triggers a click after 3 seconds of hovering"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.click)  # Connect timeout to click event
        self.hovered = False

    def enterEvent(self, event):
        """Start timer when mouse enters"""
        self.hovered = True
        self.timer.start(1000)  # 1 seconds delay
        self.update()

    def leaveEvent(self, event):
        """Stop timer when mouse leaves"""
        self.hovered = False
        self.timer.stop()
        self.update()

    def paintEvent(self, event):
        """Custom painting to change background color when hovered"""
        painter = QPainter(self)
        if self.hovered:
            painter.fillRect(self.rect(), QColor(102, 178, 255))  # Light blue background
        super().paintEvent(event)  # Default button painting