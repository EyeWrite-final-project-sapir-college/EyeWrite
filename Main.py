import sys
import threading
import keyboard
import mediapipe  # must be before PyQt6
import numpy as np
from PyQt6.QtWidgets import QApplication
import Identification
import Calibration
import cv2
import Demo
import StartMenu

# Set application window dimensions
width, height = 1900, 1000

# Initialize the Qt application
app = QApplication(sys.argv)

# Prompt the user to select which keyboard mode to use
print("Which mode do you want to run?")
mode = input("Press 'F' to use the full keyboard, or any other key to demo keyboard: ").strip().lower()


# Function to run the Qt event loop in a separate thread
def runKeyboard():
    sys.exit(app.exec())


initial_flag = True  # Flag to control initial calibration and setup

while True:

    # Perform calibration and setup if this is the first loop iteration or after a reset
    if initial_flag:
        object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_point_center, screen = Calibration.calibrate(
            width, height)

        # Load the selected keyboard interface
        if mode == "f":
            window = StartMenu.MenuContainer(width, height)  # Full keyboard
        else:
            window = Demo.Ten_buttons(width, height)  # Demo keyboard

        window.show()

        # Start the Qt event loop in a new thread
        keyboard_process = threading.Thread(target=runKeyboard)
        keyboard_process.start()

        initial_flag = False

    # Run the eye tracking and face detection
    frame, eye_frame, _, _, _, previous_iris_center, previous_eye_point_center, rectangle = Identification.identify(
        False, False, object_points, relative_iris_center, initial_rvec, previous_iris_center,
        previous_eye_point_center, screen)

    # Show camera frames for debug or monitoring
    cv2.imshow('Eye Detection', frame)
    cv2.imshow('eye_frame', eye_frame)
    cv2.waitKey(1)

    # If valid eye and rectangle data exists, update the cursor position
    if (len(previous_iris_center) != 0 and len(rectangle) == 4):
        src = np.float32([
            [rectangle[0][0], rectangle[0][1]],
            [rectangle[1][0], rectangle[1][1]],
            [rectangle[2][0], rectangle[2][1]],
            [rectangle[3][0], rectangle[3][1]]
        ])
        dst = np.float32([
            [0, 0],
            [width, 0],
            [width, height],
            [0, height]
        ])

        # Create transformation matrix from rectangle to full screen
        matrix = cv2.getPerspectiveTransform(src, dst)

        # Calculate gaze offset point and transform it
        point = np.float32([[[previous_iris_center[0] - previous_eye_point_center[0],
                              previous_iris_center[1] - previous_eye_point_center[1]]]])
        transformed_point = cv2.perspectiveTransform(point, matrix)
        center = (int(transformed_point[0][0][0]), int(transformed_point[0][0][1]))

        # Update the keyboard GUI with the new cursor position
        window.update_cursor_position(center)

    # Check for ESC key to exit
    if keyboard.is_pressed("esc"):
        print("ESC pressed - exiting")
        cv2.destroyAllWindows()
        if keyboard_process is not None and keyboard_process.is_alive():
            keyboard_process.join()
        window.hide()
        break

    # Check for SPACE key to restart calibration and keyboard
    elif keyboard.is_pressed("space"):
        print("SPACE pressed - restarting system")
        cv2.destroyAllWindows()
        if keyboard_process is not None and keyboard_process.is_alive():
            keyboard_process.join()
        window.clean_text()  # Clear current keyboard content
        initial_flag = True  # Re-trigger calibration and setup
        window.hide()
        cv2.waitKey(500)