import pyautogui
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QApplication, QLabel, QSizePolicy
)
from PyQt6.QtCore import Qt
import KeyboardHoverButton
import pygame


class MenuScreen(QWidget):
    def __init__(self, stack, width, height):
        super().__init__()

        self.stack = stack  # Reference to the stacked widget for screen switching
        stack.setWindowTitle("Main Screen")  # Set window title

        self.resize(width, height)

        # Initialize and load click sound
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("audio/click.mp3")

        # Create the main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # Welcome text at the top
        self.welcome_label = QLabel("Welcome")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet("""
            QLabel {
                font-family: Courier New;
                font-size: 60px;
                color: #32849c;
            }
        """)

        main_layout.addWidget(self.welcome_label)
        main_layout.addSpacing(120)  # Add space between title and buttons

        # Message label to show when user is out of screen range
        self.message_label = QLabel('', self)
        self.message_label.setStyleSheet("""
            color: black;
            font-size: 40px;
            font-weight: bold;
            background-color: rgba(255, 255, 255, 180); /* white with slight transparency */
        """)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.hide()

        # Create the main buttons
        btn_email_address = KeyboardHoverButton.KeyboardHoverButton("Enter Email")
        btn_verify = KeyboardHoverButton.KeyboardHoverButton("Verify Calibration")

        # Set style and layout properties for all buttons
        for btn in [btn_email_address, btn_verify]:
            btn.setMinimumSize(275, 275)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.setStyleSheet("""
                QPushButton {
                    border-radius: 70px;
                    background-color: #f7fafc;
                    border: 2px solid #cccccc;
                    font-size: 38px;
                    font-family: Courier New;
                }
                QPushButton:hover {
                    background-color: #b3d5e6;
                    border: 2px solid #498aab;
                }
            """)

        # Create horizontal layout for the buttons
        button_row = QHBoxLayout()
        button_row.addWidget(btn_email_address)
        button_row.addWidget(btn_verify)

        # Add button row and stretch to the main layout
        main_layout.addLayout(button_row)
        main_layout.addStretch()

        # Apply layout to the widget
        self.setLayout(main_layout)

        # Connect buttons to their actions
        # btn_reset is currently commented out
        btn_email_address.clicked.connect(lambda: (self.click_sound.play(), self.stack.setCurrentIndex(1)))
        btn_verify.clicked.connect(lambda: (self.click_sound.play(), self.start_verification_and_switch()))

    def resizeEvent(self, event):
        # Dynamically resize font based on window height
        height = self.height()
        new_font_size = int(height * 0.1)
        stylesheet = f"""
            QLabel {{
                font-size: {new_font_size}px;
                color: #32849c;
                font-family: Courier New;
            }}
        """
        self.welcome_label.setStyleSheet(stylesheet)

    def start_verification_and_switch(self):
        # Start calibration verification and switch to verification screen
        import VerifyCalibration
        verify_screen: VerifyCalibration = self.stack.widget(2)
        verify_screen.start_verification()
        self.stack.setCurrentIndex(2)

    def update_cursor_position(self, center):
        """Move the mouse cursor to the given position if it's inside the window"""
        if len(center) == 2:
            x, y = center
            if x <= 0 or y <= 0 or x >= self.width() or y >= self.height():
                print("out of the screen")
            else:
                print("OK")
                pyautogui.moveTo(x, y)
