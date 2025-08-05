from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout
import KeyboardHoverButton
import EmailBody
import VirtualKeyboard
import pygame

class EmailAddress(QWidget):
    def __init__(self, stack, width, height, email_body_screen):
        super().__init__()

        self.stack = stack
        self.resize(width, height)

        self.email_body_screen = email_body_screen

        # Initialize sound
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("audio/click.mp3")

        # Main layout
        layout = QVBoxLayout()

        # Row for text box and buttons
        top_row = QHBoxLayout()

        # Email address input text box
        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Enter an email address...")
        self.text_box.setFixedHeight(int(height * 0.15))
        self.text_box.setStyleSheet("""
            QTextEdit {
                font-size: 20px;
                font-family: Segoe UI;
            }
        """)
        top_row.addWidget(self.text_box)

        # Continue button to go to next screen
        continue_button = KeyboardHoverButton.KeyboardHoverButton("Continue")
        continue_button.setFixedSize(140, 120)
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
        continue_button.clicked.connect(self.handle_continue)
        top_row.addWidget(continue_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Gmail shortcut button
        gmail_button = KeyboardHoverButton.KeyboardHoverButton("@gmail.com")
        gmail_button.setMaximumSize(140, 120)
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
        self.keyboard = VirtualKeyboard.KeyboardApp()
        self.keyboard.text_box = self.text_box
        layout.addWidget(self.keyboard)

        self.setLayout(layout)

    def insert_text_with_sound(self, text):
        # Insert text at the end of the text box with sound feedback
        self.click_sound.stop()
        self.click_sound.play()
        cursor = self.text_box.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(text)
        self.text_box.setTextCursor(cursor)

    def handle_continue(self):
        # Transition to the email body screen
        self.click_sound.play()
        email = self.text_box.toPlainText().strip()
        self.email_body_screen.set_email_address(email)
        self.stack.setCurrentWidget(self.email_body_screen)  # move to email_body_screen
        self.text_box.clear()

    def clean_text(self):
        self.text_box.clear()
