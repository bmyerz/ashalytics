import cv2
import numpy as np
from common import Capture
from videodb import getvideopaths

# 10:48 - 11:15  (could be less)
start = 10 * 60 + 48
end = 11 * 60 + 15


class ImageSegmentation:
    def __init__(self, inputf):
        self.inputf = inputf

    def frames(self):
        for frame in self.inputf.frames():
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            cv2.imwrite("is_thresh.jpg", thresh)
            break
        yield None


cap = cv2.VideoCapture(getvideopaths()[0])
input_frames = Capture(cap, start, end)
seg = ImageSegmentation(input_frames)
[_ for _ in seg.frames()]
cap.release()

