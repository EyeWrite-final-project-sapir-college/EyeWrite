import pyautogui
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import Qt
import KeyboardHoverButton as HoverButton
import pygame
import sys
import os


class Ten_buttons(QWidget):
    def __init__(self, width, height):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Demo")
        self.resize(width, height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Load click sound safely (only if file exists)
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("audio/click.mp3") if os.path.exists("audio/click.mp3") else None

        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 10, 20, 10)

        # Read-only text display for showing typed characters
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFixedHeight(100)
        main_layout.addWidget(self.text_display)

        # Layout for keyboard buttons
        self.keyboard_layout = QVBoxLayout()
        self.keyboard_layout.setSpacing(10)
        main_layout.addLayout(self.keyboard_layout)

        # Create two rows of numeric buttons
        self.create_row(["1", "2", "3", "4", "5", "DEL"])
        self.create_row(["6", "7", "8", "9", "0"])

    def design_keyboard(self, button):
        # Set size policy and style for keyboard buttons
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button.setStyleSheet("""
                QPushButton {
                    border-radius: 12px;
                    background-color: #f7fafc;
                    border: 2px solid #cccccc;
                    font-size: 28px;
                }
                QPushButton:hover {
                    background-color: #b3d5e6;
                    border: 2px solid #498aab;
                }
            """)

    def create_row(self, button_texts):
        # Create a horizontal layout for a row of buttons
        row_layout = QHBoxLayout()
        row_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        for text in button_texts:
            button = HoverButton.KeyboardHoverButton(text)
            self.design_keyboard(button)
            button.clicked.connect(lambda _, t=text: self.handle_click(t))
            row_layout.addWidget(button)

        row_widget = QWidget()
        row_widget.setLayout(row_layout)
        self.keyboard_layout.addWidget(row_widget)

    def handle_click(self, text):
        # Handle button click: play sound and update text box
        if self.click_sound:
            self.click_sound.play()

        cursor = self.text_display.textCursor()
        if text == 'DEL':
            # Remove the previous character
            cursor.movePosition(QTextCursor.MoveOperation.PreviousCharacter, QTextCursor.MoveMode.KeepAnchor)
            cursor.removeSelectedText()
        else:
            # Append new character
            cursor.movePosition(QTextCursor.MoveOperation.End)
            cursor.insertText(text)

        self.text_display.setTextCursor(cursor)

    def update_cursor_position(self, center):
        # Move the mouse cursor to the given position if it's inside the window
        if len(center) == 2:
            x, y = center
            if x <= 0 or y <= 0 or x >= self.width() or y >= self.height():
                print("out of the screen")
            else:
                print("OK")
                pyautogui.moveTo(x, y)

    def clean_text(self):
        # Clear the text display area
        self.text_display.clear()


# Standalone demo runner
if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Ten_buttons(1900, 900)
    demo.showMaximized()
    sys.exit(app.exec())
