import cv2
import numpy as np

# Open web camera
cam = cv2.VideoCapture(0)

# Load pre-trained classifiers for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


def not_significant_height_change(previous, current, threshold):
    prev_y, prev_h = previous[1],previous[3]
    curr_y, curr_h = current[1], current[3]

    # Compute absolute percentage change
    change_y = abs(curr_y - prev_y) / max(prev_h, 1)  # Normalize by height
    change_h = abs(curr_h - prev_h) / max(prev_h, 1)

    return change_h>threshold and change_y>threshold

def not_significant_width_change(previous, current, threshold):
    prev_x, prev_w = previous[0],previous[2]
    curr_x, curr_w = current[0], current[2]

    # Compute absolute percentage change
    change_x = abs(curr_x - prev_x) / max(prev_w, 1)  # Normalize by width
    change_w = abs(curr_w - prev_w) / max(prev_w, 1)

    return change_x>threshold and change_w>threshold

# function before change
def identifyAndCalcEyeLocation (previous_eye_position, previous_face_position):
    pupilCenter = []
    eyesRectangle = []
    faceRectangle = []
    ret, frame = cam.read()
    if not ret:
        print("Failed to capture frame")
        return None, None, None, None

    # Convert the frame to grayscale (Haar cascades work better with grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Adjust rectangle dimensions
        h_shrink_factor = 0.5  # Reduce the size by 70%
        w_shrink_factor = 0.5
        temp_h = h
        temp_w = w
        h = int(h * h_shrink_factor)
        w = int(w * w_shrink_factor)
        y = y + (temp_h - h)//2# Center vertically
        x = x + (temp_w - w)

        if previous_face_position != None and previous_face_position != [] and not_significant_change(previous_face_position[0], (x, y, w, h), 0.03):
            x, y, w, h = previous_face_position[0]

        faceRectangle.append((x,y,w,h))

        # Draw rectangle around each detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Region of interest for eyes within the face
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(15, 15))

        for (ex, ey, ew, eh) in eyes:


            # Adjust identify rectangle dimensions
            h_shrink_factor = 0.5  # Reduce the size by 50%
            w_shrink_factor = 0.7  # Reduce the size by 30%
            temp_ew = ew
            temp_eh = eh
            ew = int(ew * w_shrink_factor)
            eh = int(eh * h_shrink_factor)
            ex = ex + (temp_ew - ew) // 2  # Center horizontally
            ey = ey + (temp_eh - eh) // 2  # Center vertically

            if previous_eye_position != None and previous_eye_position != [] and not_significant_change(previous_eye_position[0], (ex, ey, ew, eh), 0.2):
                ex,ey,ew,eh = previous_eye_position[0]

            eyesRectangle.append((ex, ey, ew, eh))


            # Draw identify rectangle around each detected eye
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            # Region of interest for the eye
            eye_gray = roi_gray[ey:ey + eh, ex:ex + ew]
            eye_color = roi_color[ey:ey + eh, ex:ex + ew]


            inv = cv2.bitwise_not(eye_color)
            thresh = cv2.cvtColor(inv, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((2, 2), np.uint8)
            erosion = cv2.erode(thresh, kernel, iterations=1)
            ret, thresh1 = cv2.threshold(erosion, 220, 255, cv2.THRESH_BINARY)
            cnts, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(cnts) != 0:
                c = max(cnts, key=cv2.contourArea)
                (x, y), radius = cv2.minEnclosingCircle(c)
                center = (int(x), int(y))
                pupilCenter.append(center)
                radius = int(radius)
                cv2.circle(eye_color, center, radius, (255, 0, 0), 2)
                cv2.circle(eye_color, center, 2, (0, 0, 255), -1)  # Mark center

    return pupilCenter, eyesRectangle, faceRectangle, frame
