import cv2
import numpy as np
from common import Capture
from videodb import getvideopaths
import sys

# 10:48 - 11:15  (could be less)
start = 10 * 60 + 48
end = 11 * 60 + 15


class ImageSegmentation:
    def __init__(self, inputf, dt_param=0.7):
        self.inputf = inputf
        self.dt_param = dt_param

    def frames(self):
        for frame in self.inputf.frames():
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            # invert so that background=black, object=white
            thresh = (255-thresh)
            cv2.imwrite("is00_thresh.jpg", thresh)

            # noise removal
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
            cv2.imwrite("is01_opening.jpg", opening)
            # now white covers foreground but has foreground false positives
            # may be sufficient if we don't care about separating touching objects;
            # also I think there will be cases like the spider where the threshould level
            # will lose the joints of its legs

            # black cover background with background false positives
            sure_bg = cv2.dilate(opening, kernel, iterations=3)
            cv2.imwrite("is02a_sure_bg.jpg", sure_bg)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,self.dt_param*dist_transform.max(),255,0)
            cv2.imwrite("is02b_sure_fg.jpg", sure_fg)

            # unkown region, i.e. part of image we are unsure about
            sure_fg = np.uint8(sure_fg)
            unknown = cv2.subtract(sure_bg,sure_fg)
            cv2.imwrite("is03_unknown.jpg", unknown)

            # Marker labelling
            ret, markers = cv2.connectedComponents(sure_fg)

            # Add one to all labels so that sure background is not 0, but 1
            markers = markers+1
            cv2.imwrite("is04_markers.jpg", markers)

            # Now, mark the region of unknown with zero
            markers[unknown==255] = 0
            cv2.imwrite("is05_markers_u0.jpg", markers)

            markers = cv2.watershed(frame, markers)
            frame[markers == -1] = [255,0,0]
            cv2.imwrite("is07_final.jpg", frame)

            break
        yield None


if __name__ == '__main__':
    dt_param = 0.7
    if len(sys.argv) > 1:
        dt_param = float(sys.argv[1])

    cap = cv2.VideoCapture(getvideopaths()[0])
    input_frames = Capture(cap, start, end)
    seg = ImageSegmentation(input_frames, dt_param=dt_param)
    [_ for _ in seg.frames()]
    cap.release()

