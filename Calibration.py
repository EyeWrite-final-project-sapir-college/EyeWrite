import Identification as Identify
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


# Calibrate process
def calibrate(width, height):
    eyeInitialLocation = None
    printInstructions(width,height,"Follow the dots using only your eyes. Keep your head still",3)


    # center - relative eye center identification by mid iris_left dot
    # ratio - vertical by eyeBrow height, horizontal by eye width
    image = np.zeros((height,width, 3), dtype=np.uint8)
    cv2.circle(image, (int(width/2), int(height/2)), 10, (0, 0, 255), -1)  # Red dot, radius 5
    cv2.imshow("initialization", image)
    cv2.waitKey(2000)
    _, _, iris, face, face_initial_z, eye, eyeBrow, _ = Identify.identify(True, width, height)
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
    cv2.imshow("initialization", image)
    cv2.waitKey(2000)
    _, _, iris_left, face, _, eye, eyeBrow, _ = Identify.identify(True, width, height)
    # displacement correction by face initial location
    iris_left_x = iris_left[0]+eyeInitialLocation[3][0]-eye[3][0]

    image = np.zeros((height,width, 3), dtype=np.uint8)
    cv2.circle(image, ((int(width))-20, (int(height/2))), 10, (0, 0, 255), -1)  # Red dot, radius 5
    cv2.imshow("initialization", image)
    cv2.waitKey(2000)
    _, _, iris_right, face, _, eye, eyeBrow, _ = Identify.identify(True, width, height)
    # displacement correction by face initial location
    iris_right_x = iris_right[0] + eyeInitialLocation[2][0] - eye[2][0]
    # calculate horizontal ratio by eye width
    identify_width_length = iris_right_x - iris_left_x
    eye_length = eyeInitialLocation[3][0] - eyeInitialLocation[2][0]
    identifyLengthFactor = identify_width_length/eye_length


    printInstructions(width, height, "Now follow the dots by moving your head", 3)
    # iris_left iris_right - width identification with horizontal head moving
    image = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.circle(image, (20, (int(height / 2))), 10, (0, 0, 255), -1)  # Red dot, radius 5
    cv2.imshow("initialization", image)
    cv2.waitKey(2000)
    _, _, iris_left, face, face_left_z, eye, eyeBrow, _ = Identify.identify(True, width, height)

    image = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.circle(image, ((int(width)) - 20, (int(height / 2))), 10, (0, 0, 255), -1)  # Red dot, radius 5
    cv2.imshow("initialization", image)
    cv2.waitKey(2000)
    _, _, iris_right, face, face_right_z, eye, eyeBrow, _ = Identify.identify(True, width, height)
    ratio_z_left = face_left_z[0] - face_initial_z[0]
    ratio_z_right = face_right_z[0] - face_initial_z[0]


    return center_ratio_width,identifyLengthFactor,ratio_z_left, ratio_z_right, face_initial_z

if "__main__" == __name__:
    center_ratio_width,identifyLengthFactor,ratio_z_left, ratio_z_right, face_initial_z = calibrate(1800, 900)
    while True:
        frame, eye_frame, irisCenter, _, h_, _, _, rectangle = Identify.identify(False, 1800, 900, center_ratio_width,identifyLengthFactor,ratio_z_left, ratio_z_right, face_initial_z)
        cv2.imshow('frame', frame)
        cv2.imshow('eye_frame', eye_frame)
        cv2.waitKey(1)