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

    def enterEvent(self, event):
        """Start timer when mouse enters"""
        self.timer.start(1000)  # 1 seconds delay


    def leaveEvent(self, event):
        self.timer.stop()
