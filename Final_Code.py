from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import imutils
import time
import dlib
from cv2 import cv2
import numpy as np
import RPi.GPIO as GPIO
from EAR import eye_aspect_ratio

# initialize dlib's face detector (HOG-based) and then create the
# facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./dlib_shape_predictor/shape_predictor_68_face_landmarks.dat')

print("[INFO] initializing camera...")

vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=True).start() # Raspberry Pi
time.sleep(2.0)

# 400x225 to 1024x576
frame_width = 400
frame_height = 225

# loop over the frames from the video stream
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

EYE_AR_THRESH = 0.26
MOUTH_AR_THRESH = 0.79
EYE_AR_CONSEC_FRAMES = 5
COUNTER = 0
counter0 =0

##For Buzzer
BuzzerPin = 17
song = [392]
beat = [8]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BuzzerPin, GPIO.OUT, initial=GPIO.LOW)
global Buzz
Buzz = GPIO.PWM(BuzzerPin, 440)

# grab the indexes of the facial landmarks for the mouth
(mStart, mEnd) = (49, 68)

while True:
    # grab the frame, resize and convert it to grayscale
    frame = vs.read()
    frame = imutils.resize(frame, width=frame_width, height=frame_height)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #adaptive histogram equaliztion for detection in any environment
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    #gray = cv2.equalizeHist(gray)
    size = gray.shape

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # check to see if a face was detected
    if len(rects) > 0:
        text = "{} face(s) found".format(len(rects))
        cv2.putText(frame, text, (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # loop over the face detections
    for rect in rects:
        # square box for face
        (bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
        cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH), (0, 255, 0), 1)
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        # average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0

        # compute the convex hull for the left and right eye, then
        # visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        # if eye aspect ratio<blink threshold, blink counter +=1
        if ear < EYE_AR_THRESH:
            COUNTER += 1
            counter0 += COUNTER/360
            if counter0 <= 3:
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    cv2.putText(frame, "Eyes Closed!", (500, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            elif 3 < counter0 < 8:
                if COUNTER >= EYE_AR_CONSEC_FRAMES + EYE_AR_CONSEC_FRAMES:
                    print("Sleeping")
                    Buzz.start(10)
                    #cv2.putText(frame, "Sleeping", (500, 20),
                            #cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            elif counter0 >= 14:
                GPIO.output(BuzzerPin, GPIO.LOW)
                Buzz.stop()
                print("Applying Brakes")      
        else:
            GPIO.output(BuzzerPin, GPIO.LOW)
            Buzz.stop()
            COUNTER = 0
            counter0 = 0

        # loop over the (x, y)-coordinates for the facial landmarks and draw all of them
        for (i, (x, y)) in enumerate(shape):
            if i == 33:
                # For Green color
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
            elif i == 8:
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

            elif i == 36:
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
            elif i == 45:
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
            elif i == 48:
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
            elif i == 54:
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                cv2.putText(frame, str(i + 1), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # q to exit video loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
