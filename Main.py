import sys
import threading
import mediapipe  # must be before PyQt6
import numpy as np
from PyQt6.QtWidgets import QApplication
import Identification
import Calibration
import cv2
import demo

width, height = 1900, 1000

object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_point_center,screen = Calibration.calibrate(width, height)

app = QApplication(sys.argv)
# window = Keyboard.KeyboardApp(width, height)
window = demo.Ten_buttons(width, height)
window.show()

def runKeyboard ():
    sys.exit(app.exec())
keyboard_process = threading.Thread(target=runKeyboard)
keyboard_process.start()

while True:
    frame, eye_frame, _, _, _, previous_iris_center, previous_eye_point_center, rectangle = Identification.identify(False, False, object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_point_center,screen)
    # Show the frame with detections
    cv2.imshow('Eye Detection', frame)
    cv2.imshow('eye_frame', eye_frame)
    cv2.waitKey(1)

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
        matrix = cv2.getPerspectiveTransform(src, dst)
        point = np.float32([[[previous_iris_center[0] - previous_eye_point_center[0],previous_iris_center[1] - previous_eye_point_center[1]]]])
        transformed_point = cv2.perspectiveTransform(point, matrix)
        center =(int(transformed_point[0][0][0]), int(transformed_point[0][0][1]))
        window.update_cursor_position(center)



# Release the camera and close windows
cam.release()
cv2.destroyAllWindows()