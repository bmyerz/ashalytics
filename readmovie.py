# import the necessary packages
import numpy as np
import cv2

capture_period_s = 5

cap = cv2.VideoCapture('sample_iTunes.mov')
fps = cap.get(cv2.CAP_PROP_FPS)
print "The video is {} fps".format(fps)

fn = 0
sec = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if float(fn)/fps % capture_period_s == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('frame_{0}s.jpg'.format(sec), gray)
        sec += capture_period_s

    fn += 1


cap.release()
print fn