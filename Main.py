import Identification as Identify
import cv2
import numpy as np
import time


width, height = 1500, 700

previous_eye_position = None
previous_face_position = None
while True:
    time.sleep(0.2)
    pupilCenter,previous_eye_position,previous_face_position ,frame = Identify.identifyAndCalcEyeLocation(previous_eye_position, previous_face_position)

    # Show the frame with detections
    cv2.imshow('Eye Detection', frame)
    cv2.waitKey(1)

    window = np.full((height, width, 3), 255, dtype=np.uint8)  # All values set to 255 (white)
    if(len(pupilCenter) != 0):
        w_factor = width / previous_eye_position[0][2]
        h_factor = height / previous_eye_position[0][3]
        center = (int((pupilCenter[0][0])*w_factor), int((pupilCenter[0][1])*h_factor))
        print(center)
        cv2.circle(window, center, 8, (0, 0, 255), -1)  # Mark point
    cv2.imshow('window', window)
    cv2.waitKey(1)

# Release the camera and close windows
cam.release()
cv2.destroyAllWindows()