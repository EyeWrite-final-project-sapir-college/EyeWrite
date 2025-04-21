import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QGridLayout
from PyQt6.QtCore import Qt
import KeyboardHoverButton as HoverButton
import pyautogui

class KeyboardApp(QWidget):
    def __init__(self, width, height):
        super().__init__()

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

    def clear_layout(self, layout):
        """Function to clear the layout from existing buttons"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def keyboard_first_page(self):
        buttonSize = 170
        """Function to create the keyboard buttons"""
        self.clear_layout(self.keyboard_layout)

        # row 1
        row1_buttons = ['ק', 'ר', 'א', 'ט', 'ו', 'ם', 'פ', 'DEL']
        for i, text in enumerate(row1_buttons):    #enumerate moves over the list and get both the index and the object
            button = HoverButton.KeyboardHoverButton(text)
            button.setFixedSize(buttonSize, buttonSize)
            button.clicked.connect(lambda checked, t=text: self.update_text(t))
            self.keyboard_layout.addWidget(button, 0, i)

        # row 2
        row2_buttons = ['ש', 'ד', 'ג', 'כ', 'ע', 'י', 'ח', 'ל', 'ך', 'ף']
        for i, text in enumerate(row2_buttons):
            button = HoverButton.KeyboardHoverButton(text)
            button.setFixedSize(buttonSize, buttonSize)
            button.clicked.connect(lambda checked, t=text: self.update_text(t))
            self.keyboard_layout.addWidget(button, 1, i)

        # row 3
        row3_buttons = ['ז', 'ס', 'ב', 'ה', 'נ', 'מ', 'צ', 'ת', 'ץ']
        for i, text in enumerate(row3_buttons):
            button = HoverButton.KeyboardHoverButton(text)
            button.setFixedSize(buttonSize, buttonSize)
            button.clicked.connect(lambda checked, t=text: self.update_text(t))
            self.keyboard_layout.addWidget(button, 2, i)

        # row 4
        button_123 = HoverButton.KeyboardHoverButton("123")
        button_123.setFixedSize(buttonSize, buttonSize)
        button_123.clicked.connect(self.keyboard_second_page)

        button_dot = HoverButton.KeyboardHoverButton(".")
        button_dot.setFixedSize(buttonSize, buttonSize)
        button_dot.clicked.connect(lambda checked, text=".": self.update_text(text))

        button_space = HoverButton.KeyboardHoverButton("רווח")
        button_space.setFixedSize(700, buttonSize)
        button_space.clicked.connect(lambda checked, text="רווח": self.update_text(text))

        button_enter = HoverButton.KeyboardHoverButton("שורה חדשה")
        button_enter.setFixedSize(buttonSize, buttonSize)
        button_enter.clicked.connect(lambda checked, text="שורה חדשה": self.update_text(text))

        self.keyboard_layout.addWidget(button_123, 3, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)
        self.keyboard_layout.addWidget(button_dot, 3, 7, 1, 1, Qt.AlignmentFlag.AlignHCenter)
        self.keyboard_layout.addWidget(button_space, 3, 1, 1, 6, Qt.AlignmentFlag.AlignHCenter)
        self.keyboard_layout.addWidget(button_enter, 3, 8, 1, 1, Qt.AlignmentFlag.AlignHCenter)

    def keyboard_second_page(self):
        buttonSize = 170
        """Function for the second keyboard page"""
        self.clear_layout(self.keyboard_layout)
        # row 1
        row1_buttons = ['1', '2', '3', '4', '5', '6', '7', '8','9','0']
        for i, text in enumerate(row1_buttons):    #enumerate moves over the list and get both the index and the object
            button = HoverButton.KeyboardHoverButton(text)
            button.setFixedSize(buttonSize, buttonSize)
            button.clicked.connect(lambda checked, t=text: self.update_text(t))
            self.keyboard_layout.addWidget(button, 0, i)

        # row 2
        row2_buttons = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        for i, text in enumerate(row2_buttons):
            button = HoverButton.KeyboardHoverButton(text)
            button.setFixedSize(buttonSize, buttonSize)
            button.clicked.connect(lambda checked, t=text: self.update_text(t))
            self.keyboard_layout.addWidget(button, 1, i)

        # row 3
        row3_buttons = ['-', '_', '=', '+', '/','[', ']', '{', '}','DEL']
        for i, text in enumerate(row3_buttons):
            button = HoverButton.KeyboardHoverButton(text)
            button.setFixedSize(buttonSize, buttonSize)
            button.clicked.connect(lambda checked, t=text: self.update_text(t))
            self.keyboard_layout.addWidget(button, 2, i)

        # row 4
        button_abc = HoverButton.KeyboardHoverButton("ABC")
        button_abc.setFixedSize(buttonSize, buttonSize)
        button_abc.clicked.connect(self.keyboard_first_page)

        button_dot = HoverButton.KeyboardHoverButton(".")
        button_dot.setFixedSize(buttonSize, buttonSize)
        button_dot.clicked.connect(lambda checked, text=".": self.update_text(text))

        button_space = HoverButton.KeyboardHoverButton("רווח")
        button_space.setFixedSize(700, buttonSize)
        button_space.clicked.connect(lambda checked, text="רווח": self.update_text(text))

        button_enter = HoverButton.KeyboardHoverButton("שורה חדשה")
        button_enter.setFixedSize(buttonSize, buttonSize)
        button_enter.clicked.connect(lambda checked, text="שורה חדשה": self.update_text(text))

        self.keyboard_layout.addWidget(button_abc, 3, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)
        self.keyboard_layout.addWidget(button_dot, 3, 7, 1, 1, Qt.AlignmentFlag.AlignHCenter)
        self.keyboard_layout.addWidget(button_space, 3, 1, 1, 6, Qt.AlignmentFlag.AlignHCenter)
        self.keyboard_layout.addWidget(button_enter, 3, 8, 1, 1, Qt.AlignmentFlag.AlignHCenter)


    def update_text(self, text):
        """Update the text box with the selected character"""
        current_text = self.text_box.toPlainText()
        if text == 'DEL':
            self.text_box.setPlainText(current_text[:-1])
        elif text == 'רווח':
            self.text_box.setPlainText(current_text + ' ')
        elif text == 'שורה חדשה':
            self.text_box.setPlainText(current_text + '\n')
        # elif text=='123':
        #     self.clear_layout(self.keyboard_layout)
        #     button_abc.clicked.connect(self.keyboard_second_page)
        #     # self.layout(keyboard_second_page)
        # elif text=='ABC':
        #     self.clear_layout(self.keyboard_layout)
        #     button_123.clicked.connect(self.keyboard_first_page)
        else:
            self.text_box.setPlainText(current_text + text)

    def update_cursor_position(self, center):
        """Move the cursor to a given position"""
        if len(center) == 2:
            pyautogui.moveTo(center[0], center[1])
