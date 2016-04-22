# import the necessary packages
import numpy as np
import cv2

cap = cv2.VideoCapture('sample_iTunes.mov')

for i in range(0, 1000):
    if i % 100 == 0:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('frame_{0}.jpg'.format(i), frame)


cap.release()