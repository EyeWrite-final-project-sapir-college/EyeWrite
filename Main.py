import sys
import threading

from PyQt6.QtWidgets import QApplication

import Identification as Identify
import cv2
import numpy as np
import time
import multiprocessing

import Keyboard

width, height = 1800, 900

previous_eye_position = None
previous_face_position = None

app = QApplication(sys.argv)
window = Keyboard.KeyboardApp()
window.show()

def runKeyboard ():
    sys.exit(app.exec())

keyboard_process = threading.Thread(target=runKeyboard)
keyboard_process.start()

while True:
    time.sleep(0.1)

    pupilCenter,previous_eye_position,previous_face_position ,frame = Identify.identifyAndCalcEyeLocation(previous_eye_position, previous_face_position)

    # Show the frame with detections
    cv2.imshow('Eye Detection', frame)
    cv2.waitKey(1)


    if(len(pupilCenter) != 0):
        w_factor = width / previous_eye_position[0][2]
        h_factor = height / previous_eye_position[0][3]
        center = (int((pupilCenter[0][0])*w_factor), int((pupilCenter[0][1])*h_factor))
        print(center)
        window.update_cursor_position(center)

# Release the camera and close windows
cam.release()
cv2.destroyAllWindows()