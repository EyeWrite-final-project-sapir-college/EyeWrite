import Identification
import cv2
import numpy as np


# Instruction how to Calibrate
def printInstructions(width, height, main_text, countdown_start):
    # text setting
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    color = (255, 255, 255)

    # calculating main_text center
    (text_width, text_height), baseline = cv2.getTextSize(main_text, font, font_scale, thickness)
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 20

    for i in range(countdown_start, 0, -1):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.putText(image, main_text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)

        countdown_text = str(i)
        # calculating number center under main_text
        (text_width, text_height), baseline = cv2.getTextSize(countdown_text, font, font_scale, thickness)
        x_countdown = (width - text_width) // 2
        y_countdown = y + text_height + 20
        cv2.putText(image, countdown_text, (x_countdown, y_countdown), font, font_scale, color, thickness, cv2.LINE_AA)

        cv2.imshow("initialization", image)
        cv2.waitKey(1000)


def getIdetification(point, width, height, center_initialization_flag, rectangle_initialization_flag, object_points = None, relative_iris_center = None, initial_rvec = None):
    for i in range(0,3):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.circle(image, (point[0], point[1]), 5*(5-i), (0, 0, 255), -1)  # Red dot, radius 5
        cv2.imshow("initialization", image)
        cv2.waitKey(1000)
    if center_initialization_flag:
        _, eye_frame, object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_center, _ = Identification.identify(True, rectangle_initialization_flag, object_points, relative_iris_center, initial_rvec)
    else:
        _, eye_frame, _, _, _, previous_iris_center, previous_eye_center, _ = Identification.identify(False, rectangle_initialization_flag, object_points, relative_iris_center,initial_rvec)
    for i in range(0,20):
        smaller_frame, eye_frame, _, _, _, previous_iris_center, previous_eye_center, _ = Identification.identify(False, False, object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_center)
        cv2.waitKey(10)
    return smaller_frame, eye_frame, object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_center


# Calibrate process
def calibrate(width, height):
    screen = []
    printInstructions(width,height,"Follow the dots using only your eyes. Keep your head still",3)

    # center - relative eye center identification by mid iris_left dot
    # ratio - vertical by eyeBrow height, horizontal by eye width
    _, eye_frame, object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_center = getIdetification((int(width / 2), int(height / 2)), width, height, True,True)

    # iris_left iris_right - width identification
    # ratio - horizontal by eye width
    _, eye_frame_top_left, _, _, _, iris_center_top_left, eye_point_center_top_left = getIdetification((50, 50), width,height, False,True,object_points,relative_iris_center,initial_rvec)
    screen.append((iris_center_top_left[0]-eye_point_center_top_left[0],iris_center_top_left[1]-eye_point_center_top_left[1]))
    _, eye_frame_top_right, _, _, _, iris_center_top_right, eye_point_center_top_right = getIdetification((width - 50, 50), width, height, False, True, object_points, relative_iris_center, initial_rvec)
    screen.append((iris_center_top_right[0] - eye_point_center_top_right[0],iris_center_top_right[1] - eye_point_center_top_right[1]))

    # iris_up iris_down - height  identification
    _, eye_frame_down_right, _, _, _, iris_center_down_right, eye_point_center_down_right = getIdetification((width - 50, height - 50), width, height, False, True, object_points, relative_iris_center, initial_rvec)
    screen.append((iris_center_down_right[0] - eye_point_center_down_right[0],iris_center_down_right[1] - eye_point_center_down_right[1]))
    _, eye_frame_down_left, _, _, _, iris_center_down_left, eye_point_center_down_left = getIdetification((50, height - 50), width, height, False, True, object_points, relative_iris_center, initial_rvec)
    screen.append((iris_center_down_left[0] - eye_point_center_down_left[0],iris_center_down_left[1] - eye_point_center_down_left[1]))
    cv2.imshow('eye_frame_center', eye_frame)
    cv2.imshow('eye_frame_left_top', eye_frame_top_left)
    cv2.imshow('eye_frame_right_top', eye_frame_top_right)
    cv2.imshow('eye_frame_right_down', eye_frame_down_right)
    cv2.imshow('eye_frame_left_down', eye_frame_down_left)
    cv2.waitKey(1)


    return object_points, relative_iris_center, initial_rvec,previous_iris_center, previous_eye_center, screen

if "__main__" == __name__:
    object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_point_center,screen = calibrate(1800, 900)
    while True:
        smaller_frame, eye_frame, object_points, _, _, previous_iris_center, previous_eye_point_center, _ = Identification.identify(False, False, object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_point_center, screen)
        cv2.imshow('frame', smaller_frame)
        cv2.imshow('eye_frame', eye_frame)
        cv2.waitKey(1)