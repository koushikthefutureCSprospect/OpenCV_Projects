""" 
from __future__ import print_function
from mediapipe.tasks import python 
from mediapipe.tasks.python import vision
import serial 
import time
import cv2
import mediapipe as mp
import keyboard
import numpy as np
import math

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

arduino = serial.Serial(port='COM25', baudrate=230400, timeout=.1)

connections = [
    (0,1),(1,2),(2,3),(3,4), #Connections for thumb
    (0,5),(5,6),(6,7),(7,8), #Connections for pointer
    (5,9),(9,10),(10,11),(11,12), #Connections for middle
    (9,13),(13,14),(14,15),(15,16), #Connections for ring
    (13,17),(17,18),(18,19),(19,20), #Connections for Pinky
    (0,17),(0,9),(0,13) #Palm
]


def write_read(x):
    arduino.write(bytes(x,  'utf-8'))
    
    time.sleep(1)
    #data = arduino.readline()
    #return  data


while True:
    ref, frame = cap.read()
    if ref == False:
        continue 
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)



    frames = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgbFrame)
    h,w,c = frame.shape
    detection_result = detector.detect(frames)

    if detection_result.hand_landmarks:
        for hl in detection_result.hand_landmarks:
            points = []
            index = hl[8]
            thumb = hl[4]
            for lm in hl:
                cx, cy = int(lm.x*w), int(lm.y*h)
                points.append((cx,cy))
                cv2.circle(frame,(cx,cy),5,(0,0,255),cv2.FILLED)
            ix, iy = int(index.x*w), int(index.y*h)
            tx, ty = int(thumb.x*w), int(thumb.y*h)
            cv2.circle(frame,(ix,iy),8,(0,0,0),cv2.FILLED)
            cv2.circle(frame,(tx,ty),8,(0,0,0),cv2.FILLED)
            for start, end in connections:
                cv2.line(frame,points[start],points[end],(0,255,0),2)
            cv2.line(frame,(ix,iy),(tx,ty),(255,255,255),2) 
            distance = math.dist((ix,iy),(tx,ty))
            write_read(str(distance))
            #print(distance)
    
    cv2.rectangle(frame,(50,50),(200,20),(255,255,255), -1)




    cv2.imshow("Camera Feed", frame)
    cv2.waitKey(1)
"""

from __future__ import print_function
from mediapipe.tasks import python 
from mediapipe.tasks.python import vision
import serial 
import time
import cv2
import mediapipe as mp
import keyboard
import numpy as np
import math

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

arduino = serial.Serial(port='COM25', baudrate=230400, timeout=.1)

connections = [
    (0,1),(1,2),(2,3),(3,4), #Connections for thumb
    (0,5),(5,6),(6,7),(7,8), #Connections for pointer
    (5,9),(9,10),(10,11),(11,12), #Connections for middle
    (9,13),(13,14),(14,15),(15,16), #Connections for ring
    (13,17),(17,18),(18,19),(19,20), #Connections for Pinky
    (0,17),(0,9),(0,13) #Palm
]

def write_read(x):
    # Added a newline character '\n' so the Arduino knows exactly where a message ends
    arduino.write(bytes(x, 'utf-8')) 

# --- Timing Variables for Non-Blocking Rate Limiting ---
last_send_time = 0
send_interval = 0.05  # Send data every 0.05 seconds (50ms = 20 updates per second)

while True:
    ref, frame = cap.read()
    if not ref:
        continue 
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frames = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgbFrame)
    h, w, c = frame.shape
    detection_result = detector.detect(frames)

    if detection_result.hand_landmarks:
        for hl in detection_result.hand_landmarks:
            points = []
            index = hl[8]
            thumb = hl[4]
            for lm in hl:
                cx, cy = int(lm.x*w), int(lm.y*h)
                points.append((cx,cy))
                cv2.circle(frame,(cx,cy),5,(0,0,255),cv2.FILLED)
            ix, iy = int(index.x*w), int(index.y*h)
            tx, ty = int(thumb.x*w), int(thumb.y*h)
            cv2.circle(frame,(ix,iy),8,(0,0,0),cv2.FILLED)
            cv2.circle(frame,(tx,ty),8,(0,0,0),cv2.FILLED)
            for start, end in connections:
                cv2.line(frame,points[start],points[end],(0,255,0),2)
            cv2.line(frame,(ix,iy),(tx,ty),(255,255,255),2) 
            
            distance = math.dist((ix,iy),(tx,ty))
            
            # --- Non-Blocking Rate Limiter Check ---
            current_time = time.time()
            if current_time - last_send_time > send_interval:
                # Rounding the distance keeps the string small and clean over Serial
                write_read(str(round(distance, 2)))  
                last_send_time = current_time
    
    cv2.rectangle(frame,(50,50),(200,20),(255,255,255), -1)

    cv2.imshow("Camera Feed", frame)
    
    # Press 'q' on your keyboard to exit the script cleanly
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
