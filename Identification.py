import cv2
import mediapipe as mp
import numpy as np

#################### initial mediapipe and identification variables ####################

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

# change factors
factor = 0

# initial camera
cap = cv2.VideoCapture(0)
w, h = 3840, 2160
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

# camera matrix
focal_length = w
camera_matrix = np.array([
    [focal_length, 0, w / 2],
    [0, focal_length, w / 2],
    [0, 0, 1]
], dtype=np.float32)

# camera distortion
dist_coeffs = np.zeros((4, 1))

distance_head_screen = 5000

#################### main functions ####################
def initialOpMatrix (image_points, image_points_z):
    # 3D points relative to the nose
    object_points = np.array([
        [0.0, 0.0, 0.0],  # Nose tip
        [image_points[1][0] - image_points[0][0], image_points[1][1] - image_points[0][1], image_points_z[1]-image_points_z[0]],  # Right eye inner
        [image_points[2][0] - image_points[0][0], image_points[2][1] - image_points[0][1], image_points_z[2]-image_points_z[0]],  # Left eye inner
        [image_points[3][0] - image_points[0][0], image_points[3][1] - image_points[0][1], image_points_z[3]-image_points_z[0]],  # right eyeBrow outer
        [image_points[4][0] - image_points[0][0], image_points[4][1] - image_points[0][1], image_points_z[4]-image_points_z[0]],  # right eyeBrow outer
        [image_points[5][0] - image_points[0][0], image_points[5][1] - image_points[0][1], image_points_z[5]-image_points_z[0]],  # nose tip
        [image_points[6][0] - image_points[0][0], image_points[6][1] - image_points[0][1], image_points_z[6] - image_points_z[0]],  # right eyeBrow middle
        [image_points[7][0] - image_points[0][0], image_points[7][1] - image_points[0][1], image_points_z[7] - image_points_z[0]]  # right eyeBrow middle

    ], dtype=np.float32)
    return object_points


def smoothEyeDetection (new_point, exist_point, initialization_flag, alpha):
    if exist_point == None:
        return new_point

    # smoothing factor
    if initialization_flag:
        alpha = 1

    x = int(alpha * new_point[0] + (1 - alpha) * exist_point[0])
    y = int(alpha * new_point[1] + (1 - alpha) * exist_point[1])
    return (x,y)


# identify features from image by mediapipe
def identify (center_initialization_flag, initialization_flag, object_points = None, relative_iris_center = None, initial_rvec = None, previous_iris_center = None, previous_eye_point_center = None , screen = None):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.flip(frame, 1, frame)
        # resize image to 4k for getting more pixels in the eye section
        frame = cv2.resize(frame,(3840, 2160), interpolation=cv2.INTER_LINEAR)
        results = face_mesh.process(frame)
        if not results.multi_face_landmarks:
            print("can't identify face")
            continue

        # identify features
        for face_landmarks in results.multi_face_landmarks:
            iris = list(mp_face_mesh.FACEMESH_LEFT_IRIS)
            left_dot = face_landmarks.landmark[iris[0][0]] #476
            right_dot = face_landmarks.landmark[iris[3][0]] #474
            left_x, left_y = int(left_dot.x * frame.shape[1]), int(left_dot.y * frame.shape[0])
            right_x, right_y = int(right_dot.x * frame.shape[1]), int(right_dot.y * frame.shape[0])
            iris_center = (int((right_x + left_x) / 2), int((right_y + left_y) / 2))
            iris_center = smoothEyeDetection(iris_center, previous_iris_center, initialization_flag, 0.2)
            cv2.circle(frame, iris_center, 2, (0, 0, 255), -1)

            global w,h
            landmark = face_landmarks.landmark
            image_points = np.array([
                [landmark[6].x * w, landmark[6].y * h],  # Nose middle
                [landmark[133].x * w, landmark[133].y * h],  # Right eye in
                [landmark[362].x * w, landmark[362].y * h],  # Left eye in
                [landmark[70].x * w, landmark[70].y * h],  # right eyeBrow outer
                [landmark[300].x * w, landmark[300].y * h],  # left eyeBrow outer
                [landmark[1].x * w, landmark[1].y * h],  # nose tip
                [landmark[295].x * w, landmark[295].y * h],  # right eyeBrow middle
                [landmark[65].x * w, landmark[65].y * h]  # left eyeBrow middle
            ], dtype=np.float32)

            image_points_z = np.array(
                [landmark[6].z, landmark[133].z, landmark[362].z, landmark[70].z, landmark[300].z, landmark[1].z,landmark[295].z, landmark[65].z], dtype=np.float32) * distance_head_screen

            # print dots on the face
            for i in image_points:
                if (i[0] != None and i[1] != None):
                    cv2.circle(frame, (int(i[0]), int(i[1])), 4, (255, 0, 0), -1)

            if center_initialization_flag :
                object_points = initialOpMatrix (image_points, image_points_z)
                relative_iris_center = [iris_center[0] - image_points[0][0], iris_center[1] - image_points[0][1], (left_dot.z + right_dot.z)/2*distance_head_screen - image_points_z[0]]

            # calculate pose using solvePnP
            success, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)

            if success:
                R, _ = cv2.Rodrigues(rvec)
                head_pos = R @ np.array([0, 0, 0]).reshape(3, 1) + tvec
                cv2.putText(frame, f"Head Z: {head_pos[2][0]:.1f} mm", (30, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                # get relative left eye location
                eye3D = np.array(relative_iris_center, dtype=np.float32)  # לדוגמה: עין שמאל
                eye2D, _ = cv2.projectPoints(eye3D, rvec, tvec, camera_matrix, dist_coeffs)
                eye_point_center = tuple(eye2D[0][0].astype(int))

                pitch, yaw, roll = 0,0,0
                if initial_rvec is not None:
                    R_initial, _ = cv2.Rodrigues(initial_rvec)
                    R_relative  = R_initial.T @ R

                    pitch = np.arctan2(R_relative[2, 1], R_relative[2, 2])  # rotation around X-axis → up/down
                    yaw = np.arctan2(-R_relative[2, 0], np.sqrt(R_relative[0, 0] ** 2 + R_relative[1, 0] ** 2))  # Y-axis → left/right
                    roll = np.arctan2(R_relative[1, 0], R_relative[0, 0])  # rotation around Z-axis

                    # if pitch < 0:
                    #     fix_pitch_y = pitch*40 #up
                    # else:
                    #     fix_pitch_y = pitch*40 #down
                    #
                    # if yaw < 0:
                    #     fix_yaw_x = yaw * 70#65 #right
                    #     # fix_yaw_y = yaw * 25  # right
                    # else:
                    #     fix_yaw_x = yaw * 80#80 #left
                    #     # fix_yaw_y = yaw * 30  # left
                    #
                    # eye_point_center = (int(eye_point_center[0] + fix_yaw_x), int(eye_point_center[1] - fix_pitch_y))


                eye_point_center = smoothEyeDetection(eye_point_center, previous_eye_point_center, initialization_flag, 0.3)

                # print center
                cv2.circle(frame, eye_point_center, 2, (0, 255, 0), -1)


                if screen != None :
                    for i in screen:
                        x = previous_eye_point_center[0] + i[0]
                        y = previous_eye_point_center[1] + i[1]
                        cv2.circle(frame, (x,y), 2, (255, 255, 255), -1)



            #resize the image to smaller size to show it
            smaller_frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)
            eye = (int(image_points[2][0]),int(image_points[2][1]))
            eye_frame = frame[eye[1]-100 : eye[1]+100, eye[0]-100:eye[0]+300]
            cv2.putText(eye_frame, f"{int(pitch*1000)} ,{int(yaw*1000)} ,{int(roll*1000)}", (2, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            return smaller_frame, eye_frame, object_points, relative_iris_center, rvec, iris_center, eye_point_center, screen


if "__main__" == __name__:
    image = np.zeros((1000, 1900, 3), dtype=np.uint8)
    cv2.circle(image, (950, 500), 20, (0, 0, 255), -1)  # Red dot, radius 5
    cv2.imshow("initialization", image)
    cv2.waitKey(3000)
    smaller_frame, eye_frame, object_points, relative_iris_center, rvec, iris_center, eye_point_center,_ = identify(True, True)
    cv2.imshow('initial', eye_frame)
    smaller_frame, eye_frame, object_points, relative_iris_center, rvec, iris_center, eye_point_center,_ = identify(False,False, object_points, relative_iris_center, rvec, iris_center, eye_point_center)
    cv2.imshow('initial2', eye_frame)
    cv2.waitKey(1)
    while True:
        smaller_frame, eye_frame, object_points, _, _, iris_center, eye_point_center,_  = identify(False,False, object_points, relative_iris_center, rvec, iris_center, eye_point_center)
        cv2.imshow('frame', smaller_frame)
        cv2.imshow('eye_frame', eye_frame)
        cv2.waitKey(100)