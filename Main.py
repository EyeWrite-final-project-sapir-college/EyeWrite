import sys
import threading
import mediapipe  # must be before PyQt6
from PyQt6.QtWidgets import QApplication
import Calibration
import Identification as Identify
import cv2
import Keyboard

width, height = 1800, 900

center_ratio_width, centerToLeftOrRight = Calibration.calibrate(width, height)

app = QApplication(sys.argv)
window = Keyboard.KeyboardApp(width, height)
window.show()

def runKeyboard ():
    sys.exit(app.exec())
keyboard_process = threading.Thread(target=runKeyboard)
keyboard_process.start()

while True:
    frame, irisCenter, _, _, _, rectangle = Identify.identify(width, height, center_ratio_width, centerToLeftOrRight)
    # Show the frame with detections
    cv2.imshow('Eye Detection', frame)
    cv2.waitKey(1)
    print(irisCenter)

    if(len(irisCenter) != 0 and len(rectangle)==4):
        w_factor = width / rectangle[2]
        h_factor = height / rectangle[3]
        center = (int((irisCenter[0]-rectangle[0])*w_factor), int((irisCenter[1]-rectangle[1])*h_factor))
        window.update_cursor_position(center)

# Release the camera and close windows
cam.release()
cv2.destroyAllWindows()