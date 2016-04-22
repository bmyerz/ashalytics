# import the necessary packages
import numpy as np
import cv2
import imutils

# 12:15 - 12:19
start = 12 * 60 + 15
end = 12 * 60 + 19

cap = cv2.VideoCapture(
    'opendap_hyrax_large_format_RS03ASHS-PN03B-06-CAMHDA301_2016_01_01_CAMHDA301-20160101T000000Z.mov')
fps = cap.get(cv2.CAP_PROP_FPS)
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print "The video is {} fps".format(fps)

fn = 0

# seek to start
cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)

# video writer to same format (slightly different fps?)
orig_out = cv2.VideoWriter("selected_orig.avi",
                           cv2.VideoWriter_fourcc(*'MJPG'),
                           fps,
                           (int(w), int(h)))
thresh_out = None
fdelta_out = None

# use the first frame as the golden copy
firstFrame = None

while cap.isOpened() and cap.get(cv2.CAP_PROP_POS_MSEC) < end * 1000:
    ret, frame = cap.read()
    if not ret:
        break

    #cv2.imwrite('frame_{0}.jpg'.format(fn), frame)

    # resize
    resized = imutils.resize(frame, width=500)
    # convert to grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # blur so that we don't detect spurious frame-to-frame differences
    # TODO: we are sort of trying to detect a blurry entity (the emissions),
    # TODO: so have to play with the stencil size
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)

    # store first frame and initialize the writer
    if firstFrame is None:
        firstFrame = blurred
        thresh_out = cv2.VideoWriter("selected_thresh.avi",
            cv2.VideoWriter_fourcc(*'MJPG'),
            fps,
            (firstFrame.shape[1], firstFrame.shape[0])) 
        fdelta_out = cv2.VideoWriter("selected_fdelta.avi",
            cv2.VideoWriter_fourcc(*'MJPG'),
            fps,
            (firstFrame.shape[1], firstFrame.shape[0])) 
        blurred_out = cv2.VideoWriter("selected_blurred.avi",
            cv2.VideoWriter_fourcc(*'MJPG'),
            fps,
            (firstFrame.shape[1], firstFrame.shape[0])) 
        continue

    # compute the absolute difference between the current frame and
        # first frame
    frameDelta = cv2.absdiff(firstFrame, blurred)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes
    dilated = cv2.dilate(thresh, None, iterations=2)

    orig_out.write(frame)
    blurred_with_color = cv2.merge([blurred]*3)
    blurred_out.write(blurred_with_color)
    fdelta_with_color = cv2.merge([frameDelta]*3)
    fdelta_out.write(fdelta_with_color)
    thresh_with_color = cv2.merge([dilated]*3)
    thresh_out.write(thresh_with_color)

    fn += 1


cap.release()
orig_out.release()
thresh_out.release()
