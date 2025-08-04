from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
import KeyboardHoverButton
import pygame


class KeyboardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.caps_on = False  # Track the Caps Lock state

        # Initialize and load click sound
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("audio/click.mp3")

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Main vertical layout for the keyboard
        self.keyboard_layout = QVBoxLayout()
        self.keyboard_layout.setSpacing(10)
        self.keyboard_layout.setContentsMargins(20, 10, 20, 10)
        self.setLayout(self.keyboard_layout)

        self.text_box = None  # Will be externally set to the target text box
        self.keyboard_first_page()  # Show default keyboard page

    def clear_layout(self, layout):
        # Remove all widgets from the layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def design_keyboard(self, button):
        # Apply styling to a keyboard button
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button.setStyleSheet(f"""
            QPushButton {{
                border-radius: 12px;
                background-color: #f7fafc;
                border: 2px solid #cccccc;
                font-size: 28px;
            }}
            QPushButton:hover {{
                background-color: #b3d5e6;
                border: 2px solid #498aab;
            }}
        """)

    def create_centered_row(self, button_texts, on_click):
        # Create a horizontal row of keyboard buttons centered in the layout
        row_layout = QHBoxLayout()
        row_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        for text in button_texts:
            display_text = text.replace("&", "&&")  # Escape ampersands for display
            button = KeyboardHoverButton.KeyboardHoverButton(display_text)
            self.design_keyboard(button)
            button.clicked.connect(lambda checked, t=text: on_click(t))  # Bind click
            row_layout.addWidget(button)

        row_widget = QWidget()
        row_widget.setLayout(row_layout)
        self.keyboard_layout.addWidget(row_widget)

    def create_bottom_row(self, switch_button_text):
        # Create the special function row with "space", "enter", etc.
        row_layout = QHBoxLayout()
        row_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        def create_special_button(text, stretch, action):
            btn = KeyboardHoverButton.KeyboardHoverButton(text)
            self.design_keyboard(btn)
            btn.clicked.connect(action)
            container = QWidget()
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(btn)
            container.setLayout(layout)
            container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            row_layout.addWidget(container, stretch)

        create_special_button(switch_button_text, 1, lambda: self.update_text(switch_button_text))
        create_special_button(",", 1, lambda: self.update_text(","))
        create_special_button("space", 4, lambda: self.update_text("space"))
        create_special_button(".", 1, lambda: self.update_text("."))
        create_special_button("New Line", 2, lambda: self.update_text("New Line"))

        row_widget = QWidget()
        row_widget.setLayout(row_layout)
        self.keyboard_layout.addWidget(row_widget)

    def keyboard_first_page(self):
        # Default lowercase letters layout
        self.clear_layout(self.keyboard_layout)
        self.create_centered_row(['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'], self.update_text)
        self.create_centered_row(['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'], self.update_text)
        self.create_centered_row(['Caps Lock', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'DEL'], self.update_text)
        self.create_bottom_row("123")

    def keyboard_second_page(self):
        # Capital letters layout
        self.clear_layout(self.keyboard_layout)
        self.create_centered_row(['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'], self.update_text)
        self.create_centered_row(['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'], self.update_text)
        self.create_centered_row(['Caps Lock', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'DEL'], self.update_text)
        self.create_bottom_row("123")

    def keyboard_third_page(self):
        # Symbols and numbers layout
        self.clear_layout(self.keyboard_layout)
        self.create_centered_row(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], self.update_text)
        self.create_centered_row(['!', '@', '#', '$', '%', '^', '&', '*', '(', ')'], self.update_text)
        self.create_centered_row(['-', '_', '=', '+', '/', '?', '\" ', '\'', ':', 'DEL'], self.update_text)
        self.create_bottom_row("abc")

    def update_text(self, text):
        # Handle button text input logic
        self.click_sound.play()

        if self.text_box is None:
            return

        current_text = self.text_box.toPlainText()

        if text == 'DEL':
            self.text_box.setPlainText(current_text[:-1])
        elif text == 'Caps Lock':
            if not self.caps_on:
                self.caps_on = True
                self.keyboard_second_page()
            else:
                self.caps_on = False
                self.keyboard_first_page()
        elif text == '123':
            self.keyboard_third_page()
        elif text == 'abc':
            self.keyboard_first_page()
        elif text == 'space':
            self.text_box.setPlainText(current_text + ' ')
        elif text == 'New Line':
            self.text_box.setPlainText(current_text + '\n')
        else:
            self.text_box.setPlainText(current_text + text)
            # Automatically turn off caps after typing a capital letter
            if self.caps_on and text.isalpha():
                self.caps_on = False
                self.keyboard_first_page()
