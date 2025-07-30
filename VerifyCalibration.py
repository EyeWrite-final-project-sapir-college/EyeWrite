import pyautogui
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QStackedLayout
from PyQt6.QtCore import Qt, QTimer
import pygame
import KeyboardHoverButton

class VerifyCalibration(QWidget):
    def __init__(self, stack, width, height):
        super().__init__()

        self.resize(width, height)

        # Initialize click sound
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("audio/click.mp3")
        self.clicked_buttons = set()

        self.top_button = None
        self.bottom_button = None
        self.left_button = None
        self.right_button = None

        # Stacked layout to switch between screens
        self.main_layout = QStackedLayout()
        self.setLayout(self.main_layout)

        # ======== Start screen with countdown ========
        self.start_screen = QWidget()
        start_layout = QVBoxLayout()
        start_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        instruction_label = QLabel("Press all 4 buttons")
        instruction_label.setStyleSheet("font-size: 36px; font-family: Segoe UI; color: #32849c;")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.countdown_label = QLabel("")
        self.countdown_label.setStyleSheet("font-size: 60px; font-family: Segoe UI; color: #000000;")
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_layout.addWidget(instruction_label)
        start_layout.addWidget(self.countdown_label)
        self.start_screen.setLayout(start_layout)

        # ======== Button screen ========
        self.button_screen = self.create_button_screen(stack)

        # Add screens to the stacked layout
        self.main_layout.addWidget(self.start_screen)
        self.main_layout.addWidget(self.button_screen)

        # Countdown logic
        self.count = 3
        self.start_delay_timer = QTimer()
        self.start_delay_timer.setSingleShot(True)
        self.start_delay_timer.timeout.connect(self.start_countdown)

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)

    def start_verification(self):
        """Called to start the calibration process"""
        self.count = 3
        self.countdown_label.setText("")
        self.main_layout.setCurrentWidget(self.start_screen)
        self.clicked_buttons.clear()

        default_style = self.default_button_style()
        for btn in [self.top_button, self.bottom_button, self.left_button, self.right_button]:
            btn.setEnabled(True)
            btn.setStyleSheet(default_style)

        self.start_delay_timer.start(2000)  # 2-second delay before countdown

    def start_countdown(self):
        """Start the 3-second countdown before button screen appears"""
        self.countdown_label.setText(str(self.count))
        self.countdown_timer.start(1000)  # Countdown every second

    def update_countdown(self):
        """Update countdown display each second"""
        if self.count > 1:
            self.count -= 1
            self.countdown_label.setText(str(self.count))
        else:
            self.countdown_timer.stop()
            self.main_layout.setCurrentWidget(self.button_screen)

    def default_button_style(self):
        """Return the default button style"""
        return """
            QPushButton {
                background-color: #f7fafc;
                border-radius: 20px;
                border: 2px solid #cccccc;
                font-size: 28px;
                font-family: Segoe UI;
                color: black;
            }
            QPushButton:hover {
                background-color: #b3d5e6;
                border: 2px solid #498aab;
            }
        """

    def clicked_button_style(self):
        """Return the style for a button after being clicked"""
        return """
            QPushButton {
                background-color: #b3d5e6;
                border-radius: 20px;
                border: 2px solid #498aab;
                font-size: 28px;
                font-family: Segoe UI;
                color: black;
            }
        """

    def styled_button(self, stack, text):
        """Create a styled clickable button"""
        btn = KeyboardHoverButton.KeyboardHoverButton(text)
        btn.setFixedSize(180, 180)
        btn.setStyleSheet(self.default_button_style())

        def handle_click():
            if text not in self.clicked_buttons:
                self.click_sound.play()
                self.clicked_buttons.add(text)
                btn.setStyleSheet(self.clicked_button_style())
                btn.setEnabled(False)
                if len(self.clicked_buttons) == 4:
                    stack.setCurrentIndex(0)  # Return to main menu after all buttons clicked

        btn.clicked.connect(handle_click)
        return btn

    def create_button_screen(self, stack):
        """Create the layout for the 4-button calibration screen"""
        screen = QWidget()
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        screen.setContentsMargins(0, 0, 0, 0)

        def centered_container(widget, vertical=True):
            """Helper to center a widget inside a layout"""
            wrapper = QWidget()
            wrapper_layout = QVBoxLayout() if vertical else QHBoxLayout()
            wrapper_layout.setContentsMargins(0, 0, 0, 0)
            wrapper_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            wrapper_layout.addWidget(widget)
            wrapper.setLayout(wrapper_layout)
            return wrapper

        # Create and assign the directional buttons
        self.top_button = self.styled_button(stack, "Top")
        self.bottom_button = self.styled_button(stack, "Bottom")
        self.left_button = self.styled_button(stack, "Left")
        self.right_button = self.styled_button(stack, "Right")

        # Position the buttons in a 3x3 grid
        layout.addWidget(centered_container(self.top_button, vertical=True),    0, 1)
        layout.addWidget(centered_container(self.bottom_button, vertical=True), 2, 1)
        layout.addWidget(centered_container(self.left_button, vertical=False),  1, 0)
        layout.addWidget(centered_container(self.right_button, vertical=False), 1, 2)

        # Adjust spacing
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 5)
        layout.setRowStretch(2, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 5)
        layout.setColumnStretch(2, 1)

        screen.setLayout(layout)
        return screen

    def update_cursor_position(self, center):
        """Move the mouse cursor to the given position if it's inside the window"""
        if len(center) == 2:
            x, y = center
            if x <= 0 or y <= 0 or x >= self.width() or y >= self.height():
                print("out of the screen")
            else:
                print("OK")
                pyautogui.moveTo(x, y)
