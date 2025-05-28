import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QGridLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
import KeyboardHoverButton as HoverButton
import pyautogui
import pygame


pyautogui.FAILSAFE = False
class KeyboardApp(QWidget):
    def __init__(self, width, height):
        super().__init__()

        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("audio/Click.mp3")

        self.setWindowTitle("Main Screen")
        self.resize(width, height)

        # Create a text box for output
        self.text_box = QTextEdit(self)
        self.text_box.setReadOnly(True)

        # Create the main layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_box)

        # Create the keyboard layout
        self.keyboard_layout = QGridLayout()
        layout.addLayout(self.keyboard_layout)

        # Create keyboard buttons
        self.keyboard_first_page()

        self.setLayout(layout)

        self.message_label = QLabel('', self)
        self.message_label.setStyleSheet("""
                   color: black;
                   font-size: 40px;
                   font-weight: bold;
                   background-color: rgba(255, 255, 255, 180); /* white with slight transparency */
               """)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.hide()

    def clear_layout(self, layout):  # as long as there are items in the layout - keep deleting
        while layout.count():
            item = layout.takeAt(0)  # take the first widget pos 1 from layout
            widget = item.widget()   # take the QWidget from the item (buttons)
            if widget:
                widget.deleteLater()  # delete after run to not create runtime errors

    def design_keyboard(self, button):

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
        # 437e9c another option for hover border, just a little more darker
    def keyboard_first_page(self):
        buttonSize = 170
        self.clear_layout(self.keyboard_layout)

        def add_centered_row(button_texts, row_index):
            row_layout = QHBoxLayout()
            row_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            for text in button_texts:
                button = HoverButton.KeyboardHoverButton(text)
                button.setFixedSize(buttonSize, buttonSize)
                self.design_keyboard(button)
                button.clicked.connect(lambda checked, t=text: self.update_text(t))
                row_layout.addWidget(button)
            row_widget = QWidget()
            row_widget.setLayout(row_layout)
            self.keyboard_layout.addWidget(row_widget, row_index, 0, 1, 10)

        add_centered_row(['ק', 'ר', 'א', 'ט', 'ו', 'ם', 'פ', 'DEL'], 0)
        add_centered_row(['ש', 'ד', 'ג', 'כ', 'ע', 'י', 'ח', 'ל', 'ך', 'ף'], 1)
        add_centered_row(['ז', 'ס', 'ב', 'ה', 'נ', 'מ', 'צ', 'ת', 'ץ'], 2)

        # שורה 4
        row4_layout = QHBoxLayout()
        row4_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        button_123 = HoverButton.KeyboardHoverButton("123")
        button_123.setFixedSize(buttonSize, buttonSize)
        self.design_keyboard(button_123)
        button_123.clicked.connect(lambda: (
            self.click_sound.play(),
            self.keyboard_second_page()
        ))

        button_space = HoverButton.KeyboardHoverButton("רווח")
        button_space.setFixedSize(700, buttonSize)
        self.design_keyboard(button_space)
        button_space.clicked.connect(lambda checked, text="רווח": self.update_text(text))

        button_dot = HoverButton.KeyboardHoverButton(".")
        button_dot.setFixedSize(buttonSize, buttonSize)
        self.design_keyboard(button_dot)
        button_dot.clicked.connect(lambda checked, text=".": self.update_text(text))

        button_enter = HoverButton.KeyboardHoverButton("שורה חדשה")
        button_enter.setFixedSize(buttonSize, buttonSize)
        self.design_keyboard(button_enter)
        button_enter.clicked.connect(lambda checked, text="שורה חדשה": self.update_text(text))

        button_comma = HoverButton.KeyboardHoverButton(",")
        button_comma.setFixedSize(buttonSize, buttonSize)
        self.design_keyboard(button_comma)
        button_comma.clicked.connect(lambda checked, text=",": self.update_text(text))

        row4_layout.addWidget(button_123)
        row4_layout.addWidget(button_comma)
        row4_layout.addWidget(button_space)
        row4_layout.addWidget(button_dot)
        row4_layout.addWidget(button_enter)

        row4_widget = QWidget()
        row4_widget.setLayout(row4_layout)
        self.keyboard_layout.addWidget(row4_widget, 3, 0, 1, 10)

    def keyboard_second_page(self):
        buttonSize = 170
        self.clear_layout(self.keyboard_layout)

        def add_centered_row(button_texts, row_index):
            row_layout = QHBoxLayout()
            row_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            for text in button_texts:
                display_text = text.replace("&", "&&")
                button = HoverButton.KeyboardHoverButton(display_text)
                button.setFixedSize(buttonSize, buttonSize)
                self.design_keyboard(button)
                button.clicked.connect(lambda checked, t=text: self.update_text(t))
                row_layout.addWidget(button)
            row_widget = QWidget()
            row_widget.setLayout(row_layout)
            self.keyboard_layout.addWidget(row_widget, row_index, 0, 1, 10)

        add_centered_row(['1', '2', '3', '4', '5', '6', '7', '8','9','0'], 0)
        add_centered_row(['!', '@', '#', '$', '%', '^', '&', '*', '(', ')'], 1)
        add_centered_row(['-', '_', '=', '+', '/', '[', ']', '{', '}', 'DEL'], 2)

        # שורה 4
        row4_layout = QHBoxLayout()
        row4_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        button_abc = HoverButton.KeyboardHoverButton("אבג")
        button_abc.setFixedSize(buttonSize, buttonSize)
        self.design_keyboard(button_abc)
        button_abc.clicked.connect(lambda: (
            self.click_sound.play(),
            self.keyboard_first_page()
        ))

        button_space = HoverButton.KeyboardHoverButton("רווח")
        button_space.setFixedSize(700, buttonSize)
        self.design_keyboard(button_space)
        button_space.clicked.connect(lambda checked, text="רווח": self.update_text(text))

        button_dot = HoverButton.KeyboardHoverButton(".")
        button_dot.setFixedSize(buttonSize, buttonSize)
        self.design_keyboard(button_dot)
        button_dot.clicked.connect(lambda checked, text=".": self.update_text(text))

        button_enter = HoverButton.KeyboardHoverButton("שורה חדשה")
        button_enter.setFixedSize(buttonSize, buttonSize)
        self.design_keyboard(button_enter)
        button_enter.clicked.connect(lambda checked, text="שורה חדשה": self.update_text(text))

        button_comma = HoverButton.KeyboardHoverButton(",")
        button_comma.setFixedSize(buttonSize, buttonSize)
        self.design_keyboard(button_comma)
        button_comma.clicked.connect(lambda checked, text=",": self.update_text(text))

        row4_layout.addWidget(button_abc)
        row4_layout.addWidget(button_comma)
        row4_layout.addWidget(button_space)
        row4_layout.addWidget(button_dot)
        row4_layout.addWidget(button_enter)

        row4_widget = QWidget()
        row4_widget.setLayout(row4_layout)
        self.keyboard_layout.addWidget(row4_widget, 3, 0, 1, 10)

    def update_text(self, text):
        self.click_sound.play()

        current_text = self.text_box.toPlainText()
        if text == 'DEL':
            self.text_box.setPlainText(current_text[:-1])
        elif text == 'רווח':
            self.text_box.setPlainText(current_text + ' ')
        elif text == 'שורה חדשה':
            self.text_box.setPlainText(current_text + '\n')
        else:
            self.text_box.setPlainText(current_text + text)

    def update_cursor_position(self, center):
        """Move the cursor to a given position"""
        if len(center) == 2:
            x, y = center
            if x <= 0 or y <= 0 or x >= self.width() or y >= self.height():
                self.show_message("Out of range. Look at the screen to continue.")
                print(False)
            else:
                print (True)
                self.hide_message()
                pyautogui.moveTo(x, y)

    def show_message(self, text):
        self.message_label.setText(text)
        self.message_label.resize(self.width(), self.height())  # Full width, Full height
        self.message_label.move(0, 0)  # Center vertically
        self.message_label.show()

    def hide_message(self):
        self.message_label.hide()
