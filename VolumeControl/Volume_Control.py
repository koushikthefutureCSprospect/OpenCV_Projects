from __future__ import print_function
import cv2
import mediapipe as mp
from mediapipe.tasks import python 
from mediapipe.tasks.python import vision
import keyboard
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
import numpy as np
import math

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

connections = [
    (0,1),(1,2),(2,3),(3,4), #Connections for thumb
    (0,5),(5,6),(6,7),(7,8), #Connections for pointer
    (5,9),(9,10),(10,11),(11,12), #Connections for middle
    (9,13),(13,14),(14,15),(15,16), #Connections for ring
    (13,17),(17,18),(18,19),(19,20), #Connections for Pinky
    (0,17),(0,9),(0,13) #Palm
]

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
            print(distance)
            desired_vol_db = np.interp(distance,[15,200],[min_vol,max_vol])
            volume.SetMasterVolumeLevel(desired_vol_db,None)
    
    percent = volume.GetMasterVolumeLevelScalar()*100
    x_val = np.interp(percent,[0,100],[50,200])    
    cv2.rectangle(frame,(50,50),(200,20),(255,255,255), -1)
    cv2.rectangle(frame,(50,50),(int(x_val),20),(0,0,255), -1)
    cv2.putText(frame,f"{int(percent)}%",(48,46),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    print(x_val)




    cv2.imshow("Camera Feed", frame)
    cv2.waitKey(1)