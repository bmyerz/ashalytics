# import the necessary packages
import numpy as np
import cv2

cap = cv2.VideoCapture('sample_iTunes.mov.zip')

for i in range(0, 1000):
    _, _ = cap.read()

ret, frame = cap.read()

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

cv2.imwrite('frame.jpg', frame)

cap.release()