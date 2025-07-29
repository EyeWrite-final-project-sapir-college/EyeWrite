import pyautogui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout
import KeyboardHoverButton
import EmailBody
import VirtualKeyboard
import pygame

class EmailAddress(QWidget):
    def __init__(self, stack, width, height):
        super().__init__()

        self.resize(width, height)

        # Initialize sound
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("audio/click.mp3")
        self.saved_email = ""

        # Main layout
        layout = QVBoxLayout()

        # Row for text box and buttons
        top_row = QHBoxLayout()

        # Email address input text box
        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Enter an email address...")
        self.text_box.setFixedHeight(int(height * 0.15))
        self.text_box.setFixedWidth(int(width * 0.8))
        self.text_box.setStyleSheet("""
            QTextEdit {
                font-size: 20px;
                font-family: Segoe UI;
            }
        """)
        top_row.addWidget(self.text_box)

        # Continue button to go to next screen
        continue_button = KeyboardHoverButton.KeyboardHoverButton("Continue")
        continue_button.setFixedSize(130, 70)
        continue_button.setStyleSheet("""
            QPushButton {
                border-radius: 25px;
                background-color: #f7fafc;
                border: 2px solid #cccccc;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #b3d5e6;
                border: 2px solid #498aab;
            }
        """)
        continue_button.clicked.connect(lambda: self.handle_continue(stack, width, height))
        top_row.addWidget(continue_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Gmail shortcut button
        gmail_button = KeyboardHoverButton.KeyboardHoverButton("@gmail.com")
        gmail_button.setFixedSize(130, 70)
        gmail_button.setStyleSheet("""
            QPushButton {
                border-radius: 25px;
                background-color: #f7fafc;
                border: 2px solid #cccccc;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #b3d5e6;
                border: 2px solid #498aab;
            }
        """)
        gmail_button.clicked.connect(lambda: self.insert_text_with_sound("@gmail.com"))
        top_row.addWidget(gmail_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Set margins for the top row
        top_row.setContentsMargins(100, 0, 280, 0)
        layout.addLayout(top_row)

        # Virtual keyboard setup
        self.keyboard = VirtualKeyboard.KeyboardApp(width, height)
        self.keyboard.text_box = self.text_box
        layout.addWidget(self.keyboard)

        self.setLayout(layout)

    def insert_text_with_sound(self, text):
        """Insert text at the end of the text box with sound feedback"""
        self.click_sound.stop()
        self.click_sound.play()
        cursor = self.text_box.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(text)
        self.text_box.setTextCursor(cursor)

    def handle_continue(self, stack, width, height):
        """Transition to the email body screen"""
        self.click_sound.play()
        self.saved_email = self.text_box.toPlainText()

        email_body_screen = EmailBody.EmailBody(stack, width, height, self.saved_email)
        stack.addWidget(email_body_screen)  # index 3
        stack.setCurrentIndex(3)

    def update_cursor_position(self, center):
        """Move the mouse cursor to the given position if it's inside the window"""
        if len(center) == 2:
            x, y = center
            if x <= 0 or y <= 0 or x >= self.width() or y >= self.height():
                print("out of the screen")
            else:
                print("OK")
                pyautogui.moveTo(x, y)
