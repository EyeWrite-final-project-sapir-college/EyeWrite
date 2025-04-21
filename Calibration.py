import time
import Identification as Identify
import cv2
import numpy as np


def calibrate(width, height):
    eyeInitialLocation = None

    # center - relative eye center identification by mid iris_left dot
    # ratio - vertical by eyeBrow height, horizontal by eye width
    image = np.zeros((height,width, 3), dtype=np.uint8)
    cv2.circle(image, (int(width/2), int(height/2)), 10, (0, 0, 255), -1)  # Red dot, radius 5
    cv2.imshow("Window with Dot", image)
    cv2.waitKey(1)
    time.sleep(2)
    _, iris, face, eye, eyeBrow, _ = Identify.identify(width, height)
    eyeInitialLocation = eye.copy()
    # calculate horizontal ratio by eye width
    iris_left = iris[0]-eye[2][0]
    eye_length = eye[3][0] - eye[2][0]
    # calculate vertical ratio by eyeBrow height
    top = eye[2][1] - iris[1]
    eyeBrow_length = eyeBrow[1][1] - eyeBrow[0][1]
    center_ratio_width = [iris_left / eye_length,  # ratio left eye point to center width
                          top / eyeBrow_length,  # ratio left eye point to center height
                          (eye[3][0] - eye[2][0]) / (face[3][0] - face[2][0]),  # ratio face width to eye width
                          (face[2][1] - face[3][1]) / 2]  # avg face height


    # iris_left iris_right - width identification
    # ratio - horizontal by eye width
    image = np.zeros((height,width, 3), dtype=np.uint8)
    cv2.circle(image, (20, (int(height/2))), 10, (0, 0, 255), -1)  # Red dot, radius 5
    cv2.imshow("Window with Dot", image)
    cv2.waitKey(1)
    time.sleep(2)
    _, iris_left, face, eye, eyeBrow, _ = Identify.identify(width, height)
    # displacement correction by face initial location
    iris_left_x = iris_left[0]+eyeInitialLocation[3][0]-eye[3][0]


    image = np.zeros((height,width, 3), dtype=np.uint8)
    cv2.circle(image, ((int(width))-20, (int(height/2))), 10, (0, 0, 255), -1)  # Red dot, radius 5
    cv2.imshow("Window with Dot", image)
    cv2.waitKey(1)
    time.sleep(2)
    _, iris_right, face, eye, eyeBrow, _ = Identify.identify(width, height)
    # displacement correction by face initial location
    iris_right_x = iris_right[0] + eyeInitialLocation[2][0] - eye[2][0]
    # calculate horizontal ratio by eye width
    identify_width_length = iris_right_x - iris_left_x
    eye_length = eyeInitialLocation[3][0] - eyeInitialLocation[2][0]
    identifyLengthFactor = identify_width_length/eye_length


    return center_ratio_width, identifyLengthFactor

if "__main__" == __name__:
    center_ratio_width, centerToLeftOrRight = calibrate(1800, 900)
    while True:
        frame, irisCenter, _, _, _, rectangle = Identify.identify(1800, 900, center_ratio_width, centerToLeftOrRight)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)