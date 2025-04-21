import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1980)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

#                           face                 eye           eyeBrow      iris    center
previous_points = [[None,None,None,None],[None,None,None,None],[None,None],[None],[None]]  # previous identification


# Check if a significant change occurred that justifies updating the identification
def checkChanges (points, location, factor):
    for i in range(0,len(points)):
        if previous_points[location][i] == None:
            previous_points[location][i] = points[i]

        prev_x, prev_y = previous_points[location][i]

        if abs(points[i][0] - prev_x) > factor or abs(points[i][1] - prev_y) > factor:
            previous_points[location][i] = points[i]


factor = 3
iris_factor = 0

def identify (width, height, rectangle_center_ratio=None,identifyLengthFactor = None):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.flip(frame, 1, frame)
        frame = cv2.GaussianBlur(frame, (5, 5), 2)
        results = face_mesh.process(frame)
        if not results.multi_face_landmarks:
            continue

        for face_landmarks in results.multi_face_landmarks:
            face = list(mp_face_mesh.FACEMESH_FACE_OVAL)
            upDot = face_landmarks.landmark[face[11][0]]
            downDot = face_landmarks.landmark[face[6][0]]
            leftDot = face_landmarks.landmark[face[32][0]]
            rightDot = face_landmarks.landmark[face[22][0]]
            # print(leftDot.z, rightDot.z)
            face_up = (int(upDot.x * frame.shape[1]), int(upDot.y * frame.shape[0]))
            face_down = (int(downDot.x * frame.shape[1]), int(downDot.y * frame.shape[0]))
            face_left = (int(leftDot.x * frame.shape[1]), int(leftDot.y * frame.shape[0]))
            face_right = (int(rightDot.x * frame.shape[1]), int(rightDot.y * frame.shape[0]))
            checkChanges([face_up, face_down, face_left, face_right], 0, factor)
            cv2.circle(frame, previous_points[0][0], 2, (255, 0, 0), -1)
            cv2.circle(frame, previous_points[0][1], 2, (255, 0, 0), -1)
            cv2.circle(frame, previous_points[0][2], 2, (255, 0, 0), -1)
            cv2.circle(frame, previous_points[0][3], 2, (255, 0, 0), -1)

            eye = list(mp_face_mesh.FACEMESH_LEFT_EYE)
            upDot = face_landmarks.landmark[eye[10][0]]
            downDot = face_landmarks.landmark[eye[0][0]]
            leftDot = face_landmarks.landmark[eye[15][1]]
            rightDot = face_landmarks.landmark[eye[5][0]]
            eye_up = (int(upDot.x * frame.shape[1]), int(upDot.y * frame.shape[0]))
            eye_down = (int(downDot.x * frame.shape[1]), int(downDot.y * frame.shape[0]))
            eye_left = (int(leftDot.x * frame.shape[1]), int(leftDot.y * frame.shape[0]))
            eye_right = (int(rightDot.x * frame.shape[1]), int(rightDot.y * frame.shape[0]))
            checkChanges([eye_up, eye_down, eye_left, eye_right], 1, factor)
            cv2.circle(frame, previous_points[1][0], 2, (255, 0, 0), -1)
            cv2.circle(frame, previous_points[1][1], 2, (255, 0, 0), -1)
            cv2.circle(frame, previous_points[1][2], 2, (255, 0, 0), -1)
            cv2.circle(frame, previous_points[1][3], 2, (255, 0, 0), -1)

            eyeBrow = list(mp_face_mesh.FACEMESH_LEFT_EYEBROW)
            upDot = face_landmarks.landmark[eyeBrow[0][0]]
            downDot = face_landmarks.landmark[eyeBrow[5][0]]
            eyeBrow_up = (int(upDot.x * frame.shape[1]), int(upDot.y * frame.shape[0]))
            eyeBrow_down = (int(downDot.x * frame.shape[1]), int(downDot.y * frame.shape[0]))
            checkChanges([eyeBrow_up, eyeBrow_down], 2, factor)
            cv2.circle(frame, previous_points[2][0], 2, (255, 0, 0), -1)
            cv2.circle(frame, previous_points[2][1], 2, (255, 0, 0), -1)

            iris = list(mp_face_mesh.FACEMESH_LEFT_IRIS)
            leftDot = face_landmarks.landmark[iris[0][0]]
            rightDot = face_landmarks.landmark[iris[3][0]]
            left_x, left_y = int(leftDot.x * frame.shape[1]), int(leftDot.y * frame.shape[0])
            right_x, right_y = int(rightDot.x * frame.shape[1]), int(rightDot.y * frame.shape[0])
            irisCenter = (int((right_x + left_x) / 2), int((right_y + left_y) / 2))
            checkChanges([irisCenter],3, iris_factor)
            cv2.circle(frame, previous_points[3][0], 2, (0, 0, 255), -1)

            if (rectangle_center_ratio != None):
                x_center = int(previous_points[1][2][0] + (previous_points[1][3][0] - previous_points[1][2][0]) *rectangle_center_ratio[0])
                y_center = int(previous_points[1][2][1] - (previous_points[2][1][1] - previous_points[2][0][1]) *rectangle_center_ratio[1] - ((previous_points[0][2][1] - previous_points[0][3][1]) / 2 - rectangle_center_ratio[3])* rectangle_center_ratio[2])
                checkChanges([(x_center,y_center)], 4, 0)
                cv2.circle(frame, previous_points[4][0], 2, (0, 255, 0), -1)

            # Define a virtual screen rectangle using the aspect ratio obtained from calibration
            rectangle = []
            if (identifyLengthFactor != None):
                w = int(identifyLengthFactor * (previous_points[1][3][0] - previous_points[1][2][0]))
                h = int(w * (height / width))
                x = previous_points[4][0][0] - int(w / 2)
                y = previous_points[4][0][1] - int(h / 1.8)
                rectangle = [x, y, w, h]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

            return frame, previous_points[3][0], previous_points[0], previous_points[1], previous_points[2], rectangle



if "__main__" == __name__:
    while True:
        frame,_,_,_,_,_ = identify(1980,1080)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)