import cv2
import math
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

base_options = python.BaseOptions(model_asset_path=r'blaze_face_short_range.tflite')
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)


cam = cv2.VideoCapture(0)

width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    #Get live frame
    ret, frame = cam.read()
    #If empty frame then go back to the start of the loop
    if ret == False:
        continue
    
    #Get results from detector
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    result = detector.detect(mp_image)
    detections = result.detections
    if not detections:
        continue

    first_face_points = detections[0].keypoints
    print(first_face_points)
    x_val = []
    y_val = []
    for pt in first_face_points[:3]:
        #Normalized x,y points
        xn = pt.x
        yn = pt.y

        #Converting normalized points to the proper coordinate on the frame
        x_cord = int(xn*width)
        y_cord = int(yn*height)
        x_val.append(x_cord)
        y_val.append(y_cord)
        #Draw points on frame
        cv2.circle(frame, (x_cord,y_cord),(5),(0,255,0),-1)
    target_x = sum(x_val)/4
    target_y = sum(y_val)/4
    Error_x = target_x-320
    Error_y = target_y-240
    #Displays
    cv2.imshow("Feed",frame)
    #Events
    if cv2.waitKey(1) == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()