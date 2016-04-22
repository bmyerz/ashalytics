# import the necessary packages
import numpy as np
import cv2

# 12:15 - 12:19
start = 12*60 + 15
end = 12*60 + 19

cap = cv2.VideoCapture('opendap_hyrax_large_format_RS03ASHS-PN03B-06-CAMHDA301_2016_01_01_CAMHDA301-20160101T000000Z.mov')
fps = cap.get(cv2.CAP_PROP_FPS)
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print "The video is {} fps".format(fps)

fn = 0
ncaptured = 0

# seek to start
cap.set(cv2.CAP_PROP_POS_MSEC, start*1000)

# video writer to same format (slightly different fps?)
out = cv2.VideoWriter("selected.avi",
                      cv2.VideoWriter_fourcc(*'MJPG'),
                      fps,
                      (int(w), int(h)))

while cap.isOpened() and cap.get(cv2.CAP_PROP_POS_MSEC) < end*1000:
    ret, frame = cap.read()
    if not ret:
        break

    #cv2.imwrite('frame_{0}.jpg'.format(fn), frame)
    out.write(frame)
    ncaptured += 1

    fn += 1


cap.release()
out.release()
print ncaptured