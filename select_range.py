# import the necessary packages
import numpy as np
import cv2

# 12:15 - 12:19
start = 12*60 + 15
end = 12*60 + 19

cap = cv2.VideoCapture('opendap_hyrax_large_format_RS03ASHS-PN03B-06-CAMHDA301_2016_01_01_CAMHDA301-20160101T000000Z.mov')
fps = cap.get(cv2.CAP_PROP_FPS)
print "The video is {} fps".format(fps)

fn = 0
ncaptured = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    pos_in_sec = float(fn)/fps
    if pos_in_sec >= start and pos_in_sec <= end:
        cv2.imwrite('frame_{0}.jpg'.format(fn), frame)
        ncaptured += 1

    fn += 1


cap.release()
print ncaptured