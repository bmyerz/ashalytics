# import the necessary packages
import numpy as np
import cv2

capture_period_s = 5

cap = cv2.VideoCapture('sample_iTunes.mov')
fps = cap.get(cv2.CAP_PROP_FPS)

fn = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if int(float(fn)/fps) % capture_period_s == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('frame_{0}.jpg'.format(fn), frame)

    fn += 1


cap.release()