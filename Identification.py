import cv2
import mediapipe as mp

#################### initial mediapipe and identification variables ####################

# mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

# previous identification
previous_points = [[None,None,None,None], #face
                   [None,None,None,None], #left_eye
                   [None,None]] # eyeBrow

previous_iris = [None]
previous_relative_iris_center = [None]

# change factors
factor = 3
relative_iris_center_factor = 0
iris_factor = 1

# initial camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


#################### main functions ####################

def smoothEyeDetection (new_point, exist_point, alpha):
    x = int(alpha * new_point[0] + (1 - alpha) * exist_point[0])
    y = int(alpha * new_point[1] + (1 - alpha) * exist_point[1])
    return (x,y)


# Check if a significant change occurred that justifies updating the identification
def checkPreviousPointsChange (points, location, factor, alpha):
    for i in range(0,len(points)):
        if previous_points[location][i] == None:
            previous_points[location][i] = points[i]

        prev_x, prev_y = previous_points[location][i]

        if abs(points[i][0] - prev_x) > factor or abs(points[i][1] - prev_y) > factor:
            previous_points[location][i] = smoothEyeDetection(points[i], (prev_x,prev_y), alpha)


def checkPointChange (new_point, exist_point, factor, alpha):
    if (exist_point[0] == None):
        exist_point[0] = new_point[0]
    elif (abs(new_point[0][0] - exist_point[0][0]) > factor or abs(new_point[0][1] - exist_point[0][1]) > factor):
        exist_point[0] = smoothEyeDetection(new_point[0], exist_point[0], alpha)


# identify features from image by mediapipe
def identify (initialization_flag ,width, height, center_ratio_width = None,identifyLengthFactor = None,ratio_z_left = None, ratio_z_right = None, face_initial_z = None):
    # smoothing factor
    if initialization_flag:
        alpha = 1
        iris_alpha = 1
    else:
        alpha = 0.6
        iris_alpha = 0.6

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.flip(frame, 1, frame)
        # resize image to 4k for getting more pixels in the eye section
        frame = cv2.resize(frame,(3840,2160), interpolation=cv2.INTER_LINEAR)
        results = face_mesh.process(frame)
        if not results.multi_face_landmarks:
            print("can't identify face")
            continue

        # identify features
        for face_landmarks in results.multi_face_landmarks:
            face = list(mp_face_mesh.FACEMESH_FACE_OVAL)
            up_dot = face_landmarks.landmark[face[11][0]]
            down_dot = face_landmarks.landmark[face[6][0]]
            left_dot = face_landmarks.landmark[face[32][0]]
            right_dot = face_landmarks.landmark[face[22][0]]
            face_up = (int(up_dot.x * frame.shape[1]), int(up_dot.y * frame.shape[0]))
            face_down = (int(down_dot.x * frame.shape[1]), int(down_dot.y * frame.shape[0]))
            face_left = (int(left_dot.x * frame.shape[1]), int(left_dot.y * frame.shape[0]))
            face_right = (int(right_dot.x * frame.shape[1]), int(right_dot.y * frame.shape[0]))
            face_left_right_z = (left_dot.z, right_dot.z)
            checkPreviousPointsChange([face_up, face_down, face_left, face_right], 0, factor, alpha)

            eye = list(mp_face_mesh.FACEMESH_LEFT_EYE)
            up_dot = face_landmarks.landmark[eye[10][0]]
            down_dot = face_landmarks.landmark[eye[0][0]]
            left_dot = face_landmarks.landmark[eye[15][1]]
            right_dot = face_landmarks.landmark[eye[5][0]]
            eye_up = (int(up_dot.x * frame.shape[1]), int(up_dot.y * frame.shape[0]))
            eye_down = (int(down_dot.x * frame.shape[1]), int(down_dot.y * frame.shape[0]))
            eye_left = (int(left_dot.x * frame.shape[1]), int(left_dot.y * frame.shape[0]))
            eye_right = (int(right_dot.x * frame.shape[1]), int(right_dot.y * frame.shape[0]))
            checkPreviousPointsChange([eye_up, eye_down, eye_left, eye_right], 1, factor, alpha)

            eyeBrow = list(mp_face_mesh.FACEMESH_LEFT_EYEBROW)
            up_dot = face_landmarks.landmark[eyeBrow[0][0]]
            down_dot = face_landmarks.landmark[eyeBrow[5][0]]
            eyeBrow_up = (int(up_dot.x * frame.shape[1]), int(up_dot.y * frame.shape[0]))
            eyeBrow_down = (int(down_dot.x * frame.shape[1]), int(down_dot.y * frame.shape[0]))
            checkPreviousPointsChange([eyeBrow_up, eyeBrow_down], 2, factor, alpha)

            iris = list(mp_face_mesh.FACEMESH_LEFT_IRIS)
            left_dot = face_landmarks.landmark[iris[0][0]]
            right_dot = face_landmarks.landmark[iris[3][0]]
            left_x, left_y = int(left_dot.x * frame.shape[1]), int(left_dot.y * frame.shape[0])
            right_x, right_y = int(right_dot.x * frame.shape[1]), int(right_dot.y * frame.shape[0])
            irisCenter = (int((right_x + left_x) / 2), int((right_y + left_y) / 2))
            checkPointChange([irisCenter],previous_iris,iris_factor, iris_alpha)
            cv2.circle(frame, previous_iris[0], 2, (0, 0, 255), -1)

            # print dots on the face
            for i in previous_points:
                for j in i:
                    if (j != None):
                        cv2.circle(frame, j, 2, (255, 0, 0), -1)


            # Define relative eye center point
            if (center_ratio_width != None):
                x_center = int(previous_points[1][2][0] + (previous_points[1][3][0] - previous_points[1][2][0]) *center_ratio_width[0])
                y_center = int(previous_points[1][2][1] - (previous_points[2][1][1] - previous_points[2][0][1]) *center_ratio_width[1] - ((previous_points[0][2][1] - previous_points[0][3][1]) / 2 - center_ratio_width[3])* center_ratio_width[2])
                checkPointChange([(x_center,y_center)], previous_relative_iris_center, relative_iris_center_factor,1)
                cv2.circle(frame, previous_relative_iris_center[0], 2, (0, 255, 0), -1)


            # Define a virtual screen rectangle using the aspect ratio obtained from calibration
            rectangle = []
            if (identifyLengthFactor != None and ratio_z_left != None and ratio_z_right != None and face_initial_z != None):
                w = int(identifyLengthFactor * (previous_points[1][3][0] - previous_points[1][2][0]))
                h = int(w * (height / width))
                if (face_initial_z[0] - face_left_right_z[0] < 0):
                    print(True)
                    horizontal_head_angle_adjustment = int(w / (2 * ratio_z_left) * (face_left_right_z[0] - face_initial_z[0]))
                else:
                    horizontal_head_angle_adjustment = int(w / (2 * ratio_z_right) * (face_left_right_z[1] - face_initial_z[0]))

                x = previous_relative_iris_center[0][0] - int(w / 2) + horizontal_head_angle_adjustment
                y = previous_relative_iris_center[0][1] - int(h / 1.8)
                rectangle = [x, y, w, h]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

            #resize the image to smaller size to show it
            smaller_frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)
            eye_frame = frame[previous_points[1][0][1]-100:previous_points[1][1][1]+100, previous_points[1][2][0]-100:previous_points[1][3][0]+100 ]


            return smaller_frame, eye_frame, previous_iris[0], previous_points[0], face_left_right_z, previous_points[1], previous_points[2], rectangle


if "__main__" == __name__:
    while True:
        frame, eye_frame,_,_,_,_,_,_ = identify(False, 1800,900)
        cv2.imshow('frame', frame)
        cv2.imshow('eye_frame', eye_frame)
        cv2.waitKey(1)