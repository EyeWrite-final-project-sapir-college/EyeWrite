import cv2
import mediapipe as mp
import numpy as np

#------------------- Initialize MediaPipe FaceMesh and Camera -------------------

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Initialize webcam (default camera)
try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Cannot open webcam")
except Exception as e:
    print("Camera initialization failed:", e)
    exit(1)

w, h = 3840, 2160  # Set 4K resolution for better accuracy
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

# Define intrinsic camera matrix, Approximate focal length in pixels
focalLength = 0.5 * (w + h)
camera_matrix = np.array([
    [focalLength, 0, w / 2],
    [0, focalLength, h / 2],
    [0, 0, 1]
], dtype=np.float32)

# Assuming no lens distortion
dist_coeffs = np.zeros((4, 1))

# Used for converting z-coordinates to mm
distance_head_screen = 5000


#------------------- Helper Functions -------------------

def initialOpMatrix(image_points, image_points_z):
    # Create 3D object points relative to the nose tip for pose estimation.
    object_points = np.array([
        [0.0, 0.0, 0.0],  # Nose tip (origin)
        [image_points[1][0] - image_points[0][0], image_points[1][1] - image_points[0][1], image_points_z[1] - image_points_z[0]],
        [image_points[2][0] - image_points[0][0], image_points[2][1] - image_points[0][1], image_points_z[2] - image_points_z[0]],
        [image_points[3][0] - image_points[0][0], image_points[3][1] - image_points[0][1], image_points_z[3] - image_points_z[0]],
        [image_points[4][0] - image_points[0][0], image_points[4][1] - image_points[0][1], image_points_z[4] - image_points_z[0]],
        [image_points[5][0] - image_points[0][0], image_points[5][1] - image_points[0][1], image_points_z[5] - image_points_z[0]],
        [image_points[6][0] - image_points[0][0], image_points[6][1] - image_points[0][1], image_points_z[6] - image_points_z[0]],
        [image_points[7][0] - image_points[0][0], image_points[7][1] - image_points[0][1], image_points_z[7] - image_points_z[0]]
    ], dtype=np.float32)
    return object_points


def smoothEyeDetection(new_point, exist_point, initialization_flag, alpha):
    # Smooth the movement of the eye center using exponential moving average.
    # We perform an exponential smoothing calculation in order to converge quickly when the difference is large,
    # and converge more slowly when the difference is small.
    if exist_point is None:
        return new_point
    if initialization_flag:
        alpha = 1  # No smoothing on first detection

    x = int(alpha * new_point[0] + (1 - alpha) * exist_point[0])
    y = int(alpha * new_point[1] + (1 - alpha) * exist_point[1])
    return (x, y)


#------------------- Main Function: identify -------------------

def identify(center_initialization_flag, initialization_flag,
             object_points=None, relative_iris_center=None,
             initial_rvec=None, previous_iris_center=None,
             previous_eye_point_center=None, screen=None):

    # enable to open the camera
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame")
            break

        # Flip and resize the frame for better eye resolution
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (3840, 2160), interpolation=cv2.INTER_LINEAR)

        # Run FaceMesh detection
        results = face_mesh.process(frame)
        if not results.multi_face_landmarks:
            print("Can't identify face")
            continue

        for face_landmarks in results.multi_face_landmarks:
            # Get iris landmarks and calculate center
            iris = list(mp_face_mesh.FACEMESH_LEFT_IRIS)
            left_dot = face_landmarks.landmark[iris[0][0]]
            right_dot = face_landmarks.landmark[iris[3][0]]
            left_x, left_y = int(left_dot.x * frame.shape[1]), int(left_dot.y * frame.shape[0])
            right_x, right_y = int(right_dot.x * frame.shape[1]), int(right_dot.y * frame.shape[0])
            iris_center = ((left_x + right_x) // 2, (left_y + right_y) // 2)

            # Smooth iris center
            iris_center = smoothEyeDetection(iris_center, previous_iris_center, initialization_flag, 0.2)
            cv2.circle(frame, iris_center, 2, (0, 0, 255), -1)

            global w, h
            landmark = face_landmarks.landmark

            # 2D points for solvePnP
            image_points = np.array([
                [landmark[6].x * w, landmark[6].y * h],     # Nose middle
                [landmark[133].x * w, landmark[133].y * h], # Right eye inner
                [landmark[362].x * w, landmark[362].y * h], # Left eye inner
                [landmark[70].x * w, landmark[70].y * h],   # Right eyebrow outer
                [landmark[300].x * w, landmark[300].y * h], # Left eyebrow outer
                [landmark[1].x * w, landmark[1].y * h],     # Nose tip
                [landmark[295].x * w, landmark[295].y * h], # Right eyebrow middle
                [landmark[65].x * w, landmark[65].y * h],   # Left eyebrow middle
            ], dtype=np.float32)

            image_points_z = np.array(
                [landmark[6].z, landmark[133].z, landmark[362].z, landmark[70].z,
                 landmark[300].z, landmark[1].z, landmark[295].z, landmark[65].z],
                dtype=np.float32) * distance_head_screen

            # Draw keypoints
            for pt in image_points:
                cv2.circle(frame, (int(pt[0]), int(pt[1])), 4, (255, 0, 0), -1)

            if center_initialization_flag:
                object_points = initialOpMatrix(image_points, image_points_z)
                relative_iris_center = [
                    iris_center[0] - image_points[0][0],
                    iris_center[1] - image_points[0][1],
                    ((left_dot.z + right_dot.z) / 2 * distance_head_screen) - image_points_z[0]
                ]

            # Estimate head pose
            success, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)

            if success:
                R, _ = cv2.Rodrigues(rvec)
                head_pos = R @ np.array([0, 0, 0]).reshape(3, 1) + tvec
                cv2.putText(frame, f"Head Z: {head_pos[2][0]:.1f} mm", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                # Project 3D iris position to 2D
                eye3D = np.array(relative_iris_center, dtype=np.float32)
                eye2D, _ = cv2.projectPoints(eye3D, rvec, tvec, camera_matrix, dist_coeffs)
                eye_point_center = tuple(eye2D[0][0].astype(int))

                # Calculate rotation difference if initial head pose exists
                pitch, yaw, roll = 0, 0, 0
                if initial_rvec is not None:
                    R_initial, _ = cv2.Rodrigues(initial_rvec)
                    R_relative = R_initial.T @ R
                    pitch = np.arctan2(R_relative[2, 1], R_relative[2, 2])
                    yaw = np.arctan2(-R_relative[2, 0], np.sqrt(R_relative[0, 0]**2 + R_relative[1, 0]**2))
                    roll = np.arctan2(R_relative[1, 0], R_relative[0, 0])

                # Smooth eye center
                eye_point_center = smoothEyeDetection(eye_point_center, previous_eye_point_center, initialization_flag, 0.3)
                cv2.circle(frame, eye_point_center, 2, (0, 255, 0), -1)

                # Optional visualization of gaze path
                if screen is not None:
                    for i in screen:
                        x = previous_eye_point_center[0] + i[0]
                        y = previous_eye_point_center[1] + i[1]
                        cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)

            # Crop eye region
            smaller_frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)
            eye = (int(image_points[2][0]), int(image_points[2][1]))
            try:
                eye_frame = frame[eye[1] - 100: eye[1] + 100, eye[0] - 100: eye[0] + 300]
            except Exception as e:
                print("Eye frame crop failed:", e)
                continue

            cv2.putText(eye_frame, f"{int(pitch*1000)} ,{int(yaw*1000)} ,{int(roll*1000)}", (2, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            return smaller_frame, eye_frame, object_points, relative_iris_center, rvec, iris_center, eye_point_center, screen


#------------------- Test Run -------------------

if __name__ == "__main__":
    image = np.zeros((1000, 1900, 3), dtype=np.uint8)
    cv2.circle(image, (950, 500), 20, (0, 0, 255), -1)
    cv2.imshow("initialization", image)
    cv2.waitKey(3000)

    # Initial detection
    smaller_frame, eye_frame, object_points, relative_iris_center, rvec, iris_center, eye_point_center, _ = identify(True, True)
    cv2.imshow('initial', eye_frame)

    # Second pass (for pose stabilization)
    smaller_frame, eye_frame, object_points, relative_iris_center, rvec, iris_center, eye_point_center, _ = identify(False, False, object_points,relative_iris_center,rvec, iris_center,eye_point_center)
    cv2.imshow('initial2', eye_frame)

    while True:
        smaller_frame, eye_frame, object_points, relative_iris_center, rvec, iris_center, eye_point_center, _ = identify(False, False, object_points,relative_iris_center,rvec, iris_center,eye_point_center)
        cv2.imshow('frame', smaller_frame)
        cv2.imshow('eye_frame', eye_frame)
        cv2.waitKey(100)
