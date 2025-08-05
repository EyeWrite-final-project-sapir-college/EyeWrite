from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QLabel, QSizePolicy
import VirtualKeyboard
import KeyboardHoverButton
import pygame


class EmailBody(QWidget):
    def __init__(self, stack, width, height, email_address):
        super().__init__()

        self.resize(width, height)

        self.email_address = email_address  # Store the provided email address
        self.saved_email_body = ""  # Will hold the email body content

        # Initialize sound
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("audio/click.mp3")

        # Email label displaying the recipient address
        self.email_label = QLabel(f"To: {self.email_address}")
        self.email_label.setStyleSheet("font-size: 18px; font-family: Segoe UI; color: #333;")

        # Main vertical layout
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 10, 40, 10)  # left, top, right, bottom
        layout.setSpacing(8)
        layout.addWidget(self.email_label)

        # Row containing text box and send button
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)

        # Text box for typing the email body
        self.body_box = QTextEdit()
        self.body_box.setPlaceholderText("Type your message here...")
        self.body_box.setFixedHeight(int(height * 0.15))
        self.body_box.setStyleSheet("""
            QTextEdit {
                font-size: 20px;
                font-family: Segoe UI;
            }
        """)
        top_row.addWidget(self.body_box)

        # Send button
        send_button = KeyboardHoverButton.KeyboardHoverButton("Send mail")
        send_button.setFixedSize(140, 120)
        send_button.setStyleSheet("""
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
        send_button.clicked.connect(lambda: self.handle_continue(stack))
        top_row.addWidget(send_button, alignment=Qt.AlignmentFlag.AlignRight)

        top_row.setContentsMargins(100, 0, 280, 0)  # Padding within row
        layout.addLayout(top_row)

        # Virtual keyboard component
        self.keyboard = VirtualKeyboard.KeyboardApp()
        self.keyboard.text_box = self.body_box  # Connect keyboard to text box
        self.keyboard.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.keyboard)

        # Adjust stretch factors for layout resizing
        layout.setStretch(0, 0)  # email label
        layout.setStretch(1, 1)  # top row
        layout.setStretch(2, 3)  # keyboard


        self.setLayout(layout)



    def handle_continue(self, stack):
        # Triggered when "Send mail" is clicked
        print("continued !!")
        self.click_sound.play()
        self.saved_email_body = self.body_box.toPlainText()

        # TODO: Connect to email service and send message
        # TODO: Reset email address and body fields if needed

        self.email_address = ""
        self.saved_email_body = ""
        self.body_box.clear()
        stack.setCurrentIndex(0)  # Return to main screen
