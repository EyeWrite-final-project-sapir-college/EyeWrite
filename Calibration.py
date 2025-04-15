import time
import Identification as Identify
import cv2
import numpy as np


def calibrate(width, height):
    image = np.zeros((height,width, 3), dtype=np.uint8)
    cv2.circle(image, (int(width/2), int(height/2)), 10, (0, 0, 255), -1)  # Red dot, radius 5
    cv2.imshow("Window with Dot", image)
    cv2.waitKey(1)
    time.sleep(2)
    _, x, _, eye, eyeBrow,_ = Identify.identify(width, height)
    # calculate ratio of width eye center by the eye ratio
    left = x[0]-eye[2][0]
    length = eye[3][0] - eye[2][0]
    # calculate ratio of height eye center by the eyeBrow ratio
    top_c = eye[2][1] - x[1]
    length_c = eyeBrow[1][1] - eyeBrow[0][1]
    center_ratio_width = (left/length, top_c/length_c)


    # right left
    image = np.zeros((height,width, 3), dtype=np.uint8)
    cv2.circle(image, (20, (int(height/2))), 10, (0, 0, 255), -1)  # Red dot, radius 5
    cv2.imshow("Window with Dot", image)
    cv2.waitKey(1)
    time.sleep(2)
    _, left, _, eye, eyeBrow,_ = Identify.identify(width, height)


    image = np.zeros((height,width, 3), dtype=np.uint8)
    cv2.circle(image, ((int(width))-20, (int(height/2))), 10, (0, 0, 255), -1)  # Red dot, radius 5
    cv2.imshow("Window with Dot", image)
    cv2.waitKey(1)
    time.sleep(2)
    _, right, _, eye, eyeBrow,_ = Identify.identify(width, height)
    # calculate ratio of width identifyLength center by the eye ratio
    identifyLength = right[0] - left[0]
    length = eye[3][0] - eye[2][0]
    identifyLengthFactor = identifyLength/length

    return center_ratio_width,identifyLengthFactor

if "__main__" == __name__:
    print (calibrate(1800,900))