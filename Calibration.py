import ctypes
import Identification
import cv2
import numpy as np

# ------------------- Display instructions before calibration -------------------
def printInstructions(width, height, main_text, countdown_start, win):
    # Font settings
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    color = (255, 255, 255)

    # Calculate position to center the main text
    (text_width, text_height), baseline = cv2.getTextSize(main_text, font, font_scale, thickness)
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 20

    # Countdown display loop
    for i in range(countdown_start, 0, -1):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.putText(image, main_text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)

        countdown_text = str(i)
        (text_width, text_height), baseline = cv2.getTextSize(countdown_text, font, font_scale, thickness)
        x_countdown = (width - text_width) // 2
        y_countdown = y + text_height + 20
        cv2.putText(image, countdown_text, (x_countdown, y_countdown), font, font_scale, color, thickness, cv2.LINE_AA)

        cv2.imshow(win, image)
        cv2.waitKey(1000)

# ------------------- Run eye tracking for a specific dot position -------------------
def getIdetification(point, width, height, win, center_initialization_flag, object_points = None, relative_iris_center = None, initial_rvec = None):
    # Show a red dot with animation (shrinking)
    for i in range(0, 3):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.circle(image, (point[0], point[1]), 5*(5-i), (0, 0, 255), -1)
        cv2.imshow(win, image)
        cv2.waitKey(1000)

    # First identification step (initial vs non-initial)
    if center_initialization_flag:
        _, eye_frame, object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_center, _ = Identification.identify(True, True, object_points, relative_iris_center, initial_rvec)
    else:
        _, eye_frame, _, _, _, previous_iris_center, previous_eye_center, _ = Identification.identify(False, True, object_points, relative_iris_center, initial_rvec)

    # Perform multiple frames of identification to stabilize eye tracking
    for i in range(0, 20):
        smaller_frame, eye_frame, _, _, _, previous_iris_center, previous_eye_center, _ = Identification.identify(False, False, object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_center)
        cv2.waitKey(10)

    # Return updated calibration and tracking data
    return smaller_frame, eye_frame, object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_center

# ------------------- Main calibration function -------------------
def calibrate(width, height):
    # Set OpenCV window to maximized mode (full screen area with taskbar visible)
    win = "initialization"
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)
    hwnd = ctypes.windll.user32.FindWindowW(None, win)
    ctypes.windll.user32.ShowWindow(hwnd, 3)  # 3 = SW_MAXIMIZE

    screen = []

    # Show instructions before calibration begins
    printInstructions(width, height, "Follow the dots using only your eyes. Keep your head still", 3, win)

    # Step 1: Calibrate center of screen (reference position)
    _, eye_frame, object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_center = getIdetification((int(width / 2), int(height / 2)), width, height, win, True)

    # Step 2: Calibrate top-left corner
    _, eye_frame_top_left, _, _, _, iris_center_top_left, eye_point_center_top_left = getIdetification((50, 50), width, height, win, False, object_points, relative_iris_center, initial_rvec)
    screen.append((iris_center_top_left[0] - eye_point_center_top_left[0], iris_center_top_left[1] - eye_point_center_top_left[1]))

    # Step 3: Calibrate top-right corner
    _, eye_frame_top_right, _, _, _, iris_center_top_right, eye_point_center_top_right = getIdetification((width - 50, 50), width, height, win, False, object_points, relative_iris_center, initial_rvec)
    screen.append((iris_center_top_right[0] - eye_point_center_top_right[0], iris_center_top_right[1] - eye_point_center_top_right[1]))

    # Step 4: Calibrate bottom-right corner
    _, eye_frame_down_right, _, _, _, iris_center_down_right, eye_point_center_down_right = getIdetification((width - 50, height - 50), width, height, win, False, object_points, relative_iris_center, initial_rvec)
    screen.append((iris_center_down_right[0] - eye_point_center_down_right[0], iris_center_down_right[1] - eye_point_center_down_right[1]))

    # Step 5: Calibrate bottom-left corner
    _, eye_frame_down_left, _, _, _, iris_center_down_left, eye_point_center_down_left = getIdetification((50, height - 50), width, height, win, False, object_points, relative_iris_center, initial_rvec)
    screen.append((iris_center_down_left[0] - eye_point_center_down_left[0], iris_center_down_left[1] - eye_point_center_down_left[1]))

    # Display sample eye frames from calibration
    cv2.imshow('eye_frame_center', eye_frame)
    cv2.imshow('eye_frame_left_top', eye_frame_top_left)
    cv2.imshow('eye_frame_right_top', eye_frame_top_right)
    cv2.imshow('eye_frame_right_down', eye_frame_down_right)
    cv2.imshow('eye_frame_left_down', eye_frame_down_left)
    cv2.waitKey(1)

    # Return full calibration data
    return object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_center, screen

# ------------------- Test mode: run calibration and track gaze in real-time -------------------
if "__main__" == __name__:
    object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_point_center, screen = calibrate(1900, 900)
    while True:
        smaller_frame, eye_frame, object_points, _, _, previous_iris_center, previous_eye_point_center, _ = Identification.identify(
            False, False, object_points, relative_iris_center, initial_rvec, previous_iris_center, previous_eye_point_center, screen)
        cv2.imshow('frame', smaller_frame)
        cv2.imshow('eye_frame', eye_frame)
        cv2.waitKey(1)
