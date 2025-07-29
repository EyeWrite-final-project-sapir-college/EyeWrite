import sys
from PyQt6.QtWidgets import QStackedWidget, QApplication
import EmailAddress
import VerifyCalibration
from Menu import MenuScreen


class MenuContainer(QStackedWidget):
    def __init__(self, width, height):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Menu")
        self.resize(width, height)

        # Initialize all screens and pass the stack reference to each
        self.menu_screen = MenuScreen(self, width, height)
        self.email_screen = EmailAddress.EmailAddress(self, width, height)
        self.verify_screen = VerifyCalibration.VerifyCalibration(self, width, height)

        # Add screens to the stack
        self.addWidget(self.menu_screen)    # index 0 = main menu
        self.addWidget(self.email_screen)   # index 1 = email input screen
        self.addWidget(self.verify_screen)  # index 2 = calibration verification screen

        # Show the menu screen by default
        self.setCurrentIndex(0)
        self.show()

    # Pass eye position to the current visible screen if supported
    def update_cursor_position(self, center):
        current_widget = self.currentWidget()
        if hasattr(current_widget, "update_cursor_position"):
            current_widget.update_cursor_position(center)

    # Clear any text input on the current screen if supported
    def clean_text(self):
        current_widget = self.currentWidget()
        if hasattr(current_widget, "clean_text"):
            current_widget.clean_text()


# Standalone test for the stacked window system
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuContainer(1900, 1000)
    sys.exit(app.exec())