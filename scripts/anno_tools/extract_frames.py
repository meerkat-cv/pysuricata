import cv2
import numpy as np

cap = cv2.VideoCapture(1)

ret, frame = cap.read()

frame_num = 0
while frame is not None:
    frame_num += 1
    if frame_num % 5 == 0:
        cv2.imwrite('frame_'+str(frame_num/30).zfill(3)+'.png', frame)
    cv2.imshow('Cam', frame)
    cv2.waitKey(1)

    ret, frame = cap.read()