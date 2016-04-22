# import the necessary packages
import numpy as np
import cv2
import imutils
import os

# 12:15 - 12:19
start = 12 * 60 + 15
end = 12 * 60 + 19

basedir = '/root/data/videos'

videos = ['opendap_hyrax_large_format_RS03ASHS-PN03B-06-CAMHDA301_2016_01_01_CAMHDA301-20160101T000000Z.mp4',
          'opendap_hyrax_large_format_RS03ASHS-PN03B-06-CAMHDA301_2016_01_01_CAMHDA301-20160101T060000Z.mp4',
          'opendap_hyrax_large_format_RS03ASHS-PN03B-06-CAMHDA301_2016_01_01_CAMHDA301-20160101T180000Z.mp4',
          'opendap_hyrax_large_format_RS03ASHS-PN03B-06-CAMHDA301_2016_02_10_CAMHDA301-20160210T180000Z.mp4']
videos = [os.path.join(basedir, p) for p in videos]


class ImageUtils:
    @staticmethod
    def grayscale_to_color(im):
        return cv2.merge([im]*3)

# Iterators
class Capture(object):
    """A capture that reads frames from a video device or file,
    optionally seeking"""

    def __init__(self, capture, start_ms=None, end_ms=None):
        self.cap = capture
        self.end_ms = end_ms
        if start_ms is not None:
            self.cap.set(cv2.CAP_PROP_POS_MSEC, start_ms * 1000)

    def _reached_end(self):
        return (self.end_ms is not None) and (
            self.cap.get(cv2.CAP_PROP_POS_MSEC) >= self.end_ms * 1000)

    def frames(self):
        while self.cap.isOpened() and not self._reached_end():
            ret, frame = self.cap.read()
            if not ret:
                break

            yield frame


# Before embarking on a multi-path dataflow architecture
# consider that push-oriented has complexity when there are two inputs
# and pull-oriented has complexity when there are two outputs
# Unless you schedule appropriately, there is buffering (interesting scheduling: avoid all buffering)
#class MultiSource(object):
#    pass

#class StoreVideo(object):
#    def __init__(self, inputf, videowriter):
#        self.inputf = inputf
#        self.videowriter = videowriter
#
#    def frames(self):
#        for frame in self.inputf.frames():
#            self.videowriter.write(frame)
#
#        self.videowriter.release()


class MotionEstimation(object):
    def __init__(self, inputf, capture, name):
        self.inputf = inputf
        self.cap = capture
        self.firstFrame = None
        self.thresh_out = None
        self.fdelta_out = None
        self.blurred_out = None
        self.name = name
        w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    	self.fps = self.cap.get(cv2.CAP_PROP_FPS)
	print self.fps
        self.orig_out = cv2.VideoWriter("{}_orig.avi".format(self.name),
                           cv2.VideoWriter_fourcc(*'MJPG'),
                           self.fps,
                           (int(w), int(h)))

    def frames(self):
        for frame in self.inputf.frames():
            # resize
            resized = imutils.resize(frame, width=500)
            # convert to grayscale
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            # blur so that we don't detect spurious frame-to-frame differences
            # TODO: we are sort of trying to detect a blurry entity (the emissions),
            # TODO: so have to play with the stencil size
            blurred = cv2.GaussianBlur(gray, (21, 21), 0)

            # store first frame and initialize the writer
            if self.firstFrame is None:
                self.firstFrame = blurred
                self.thresh_out = cv2.VideoWriter("{}_thresh.avi".format(self.name),
                                             cv2.VideoWriter_fourcc(*'MJPG'),
                                             self.fps,
                                             (self.firstFrame.shape[1], self.firstFrame.shape[0]))
                self.fdelta_out = cv2.VideoWriter("{}_fdelta.avi".format(self.name),
                                             cv2.VideoWriter_fourcc(*'MJPG'),
                                             self.fps,
                                             (self.firstFrame.shape[1], self.firstFrame.shape[0]))
                self.blurred_out = cv2.VideoWriter("{}_blurred.avi".format(self.name),
                                              cv2.VideoWriter_fourcc(*'MJPG'),
                                              self.fps,
                                              (self.firstFrame.shape[1], self.firstFrame.shape[0]))
                continue

            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(self.firstFrame, blurred)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes
            dilated = cv2.dilate(thresh, None, iterations=2)

            self.orig_out.write(frame)
            blurred_with_color = ImageUtils.grayscale_to_color(blurred)
            self.blurred_out.write(blurred_with_color)
            fdelta_with_color = ImageUtils.grayscale_to_color(frameDelta)
            self.fdelta_out.write(fdelta_with_color)
            thresh_with_color = ImageUtils.grayscale_to_color(dilated)
            self.thresh_out.write(thresh_with_color)

        self.orig_out.release()
        self.fdelta_out.release()
        self.thresh_out.release()
        yield None


for v in videos:
    cap = cv2.VideoCapture(v)

    input_frames = Capture(cap, start, end)
    sink = MotionEstimation(input_frames, cap, v)

    # run to completion
    [_ for _ in sink.frames()]

    cap.release()


