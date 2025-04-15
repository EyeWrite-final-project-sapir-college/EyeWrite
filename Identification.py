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

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
def identify (width, height, rectangle_center_ratio=None,identifyLengthFactor = None):

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.flip(frame, 1, frame)
        results = face_mesh.process(frame)
        if not results.multi_face_landmarks:
            continue

        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_FACE_OVAL,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
            face = list(mp_face_mesh.FACEMESH_FACE_OVAL)
            downDot = face_landmarks.landmark[face[6][0]]
            upDot = face_landmarks.landmark[face[11][0]]
            leftDot = face_landmarks.landmark[face[32][0]]
            rightDot = face_landmarks.landmark[face[22][0]]
            face_down = (int(downDot.x * frame.shape[1]), int(downDot.y * frame.shape[0]))
            face_up = (int(upDot.x * frame.shape[1]), int(upDot.y * frame.shape[0]))
            face_left = (int(leftDot.x * frame.shape[1]), int(leftDot.y * frame.shape[0]))
            face_right = (int(rightDot.x * frame.shape[1]), int(rightDot.y * frame.shape[0]))
            cv2.circle(frame, face_down, 2, (255, 0, 0), -1)
            cv2.circle(frame, face_up, 2, (255, 0, 0), -1)
            cv2.circle(frame, face_left, 2, (255, 0, 0), -1)
            cv2.circle(frame, face_right, 2, (255, 0, 0), -1)


            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_LEFT_EYE,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
            eye = list(mp_face_mesh.FACEMESH_LEFT_EYE)
            downDot = face_landmarks.landmark[eye[0][0]]
            upDot = face_landmarks.landmark[eye[10][0]]
            rightDot = face_landmarks.landmark[eye[5][0]]
            leftDot = face_landmarks.landmark[eye[15][1]]
            eye_down = (int(downDot.x * frame.shape[1]), int(downDot.y * frame.shape[0]))
            eye_up = (int(upDot.x * frame.shape[1]), int(upDot.y * frame.shape[0]))
            eye_left = (int(leftDot.x * frame.shape[1]), int(leftDot.y * frame.shape[0]))
            eye_right = (int(rightDot.x * frame.shape[1]), int(rightDot.y * frame.shape[0]))
            cv2.circle(frame, eye_down, 2, (255, 0, 0), -1)
            cv2.circle(frame, eye_up, 2, (255, 0, 0), -1)
            cv2.circle(frame, eye_left, 2, (255, 0, 0), -1)
            cv2.circle(frame, eye_right, 2, (255, 0, 0), -1)


            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_LEFT_EYEBROW,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
            eyeBrow = list(mp_face_mesh.FACEMESH_LEFT_EYEBROW)
            downDot = face_landmarks.landmark[eyeBrow[5][0]]
            upDot = face_landmarks.landmark[eyeBrow[0][0]]
            eyeBrow_down = (int(downDot.x * frame.shape[1]), int(downDot.y * frame.shape[0]))
            eyeBrow_up = (int(upDot.x * frame.shape[1]), int(upDot.y * frame.shape[0]))
            cv2.circle(frame, eyeBrow_down, 2, (255, 0, 0), -1)
            cv2.circle(frame, eyeBrow_up, 2, (255, 0, 0), -1)



            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_LEFT_IRIS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
            iris = list(mp_face_mesh.FACEMESH_LEFT_IRIS)
            leftDot = face_landmarks.landmark[iris[0][0]]
            rightDot = face_landmarks.landmark[iris[3][0]]
            left_x, left_y = int(leftDot.x * frame.shape[1]), int(leftDot.y * frame.shape[0])
            right_x, right_y = int(rightDot.x * frame.shape[1]), int(rightDot.y * frame.shape[0])
            irisCenter = (int((right_x + left_x) / 2), int((right_y+left_y)/2))
            cv2.circle(frame, irisCenter, 2, (0, 0, 255), -1)

            rectangle = []
            if(rectangle_center_ratio!=None and identifyLengthFactor!=None):
                x_center = int(eye_left[0] + (eye_right[0] - eye_left[0]) * rectangle_center_ratio[0])
                y_center = int(eye_left[1] - (eyeBrow_down[1] - eyeBrow_up[1]) * rectangle_center_ratio[1])
                cv2.circle(frame, (x_center,y_center), 2, (0, 255, 0), -1)

                w = int(identifyLengthFactor*(eye_right[0] - eye_left[0]))
                h = int(w*(height/width))
                x = x_center-int(w/2)
                y = y_center-int(h/2)
                rectangle = [x,y,w,h]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)



        return frame, irisCenter, [face_up, face_down, face_left, face_right], [eye_up, eye_down,eye_left, eye_right], [eyeBrow_up,eyeBrow_down], rectangle

if "__main__" == __name__:
    while True:
        frame, irisCenter,_,_,_,_ = identify(1800,900)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)