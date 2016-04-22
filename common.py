import cv2

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
