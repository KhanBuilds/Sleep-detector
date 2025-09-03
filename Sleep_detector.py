import cv2
import mediapipe as mp
import serial
import math

webcam = cv2.VideoCapture(0)
mp_face = mp.solutions.face_mesh
mp_drawing= mp.solutions.drawing_utils
ardiuno = serial.Serial('com3',9600)
EAR_THRESHOLD = 0.25
CLOSED_FRAMES = 0
FRAME_THRESHOLD = 5
with mp_face.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.52) as face_mesh:
    while True:
        control, frame= webcam.read()
        if control== False:
            break
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)
        height,width,channels = frame.shape
        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                point1= face_landmarks.landmark[159]
                x1= int(point1.x * width)
                y1 = int(point1.y * height)
                cv2.circle(frame, (x1,y1), 2, (0,0,255), 3)
                point2 = face_landmarks.landmark[145]
                x2 = int(point2.x * width)
                y2 = int(point2.y * height)
                cv2.circle(frame, (x2, y2), 2, (0, 0, 255), 3)
                point3 = face_landmarks.landmark[33]
                x3 = int(point3.x * width)
                y3 = int(point3.y * height)
                cv2.circle(frame, (x3, y3), 2, (0, 0, 255), 3)
                point4 = face_landmarks.landmark[133]
                x4 = int(point4.x * width)
                y4 = int(point4.y * height)
                cv2.circle(frame, (x4, y4), 2, (0, 0, 255), 3)
                distanceRV = math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))
                distanceRH = math.sqrt(math.pow(x4-x3,2)+math.pow(y4-y3,2))
                EARR = distanceRV/distanceRH

                point5 = face_landmarks.landmark[386]
                x5 = int(point5.x * width)
                y5 = int(point5.y * height)
                cv2.circle(frame, (x5, y5), 2, (0, 0, 255), 3)
                point6= face_landmarks.landmark[374]
                x6 = int(point6.x * width)
                y6 = int(point6.y * height)
                cv2.circle(frame, (x6, y6), 2, (0, 0, 255), 3)
                point7 = face_landmarks.landmark[362]
                x7 = int(point7.x * width)
                y7 = int(point7.y * height)
                cv2.circle(frame, (x7, y7), 2, (0, 0, 255), 3)
                point8 = face_landmarks.landmark[263]
                x8 = int(point8.x * width)
                y8 = int(point8.y * height)
                cv2.circle(frame, (x8, y8), 2, (0, 0, 255), 3)
                distanceLV = math.sqrt(math.pow(x6 - x5, 2) + math.pow(y6 - y5, 2))
                distanceLH = math.sqrt(math.pow(x8 - x7, 2) + math.pow(y8 - y7, 2))
                EARL = distanceLV/distanceLH

                EAR = (EARR+EARL)/2


                if EAR >= EAR_THRESHOLD:
                    state = "Eyes Open"
                    CLOSED_FRAMES = 0  # reset when eyes are open
                    ardiuno.write(b'A')
                else:
                    CLOSED_FRAMES += 1
                    if CLOSED_FRAMES >= FRAME_THRESHOLD:
                        state = "Eyes Closed"
                        ardiuno.write(b'B')

                print(f"EAR: {EAR:.3f} | State: {state} | Closed Frames: {CLOSED_FRAMES}")

        cv2.imshow("final", frame)
        if cv2.waitKey(10) == 27:
            break

