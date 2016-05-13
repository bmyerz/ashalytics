import cv2
import os
from common import Capture
from time import time

video_root = "/root/data/videos/"


class ExtractScenes(object):
    def __init__(self):
        self._gen = None

    def getnext(self):
        try:
            return self._gen.next()
        except StopIteration:
            self._gen = None
            return None

    def _generator(self, filename, scene_bounds):
        outfiles = []
        fullpath = os.path.join(video_root, filename)

        realtime_start = time()
        total_frames = 0

        for i, s, e in scene_bounds:
            cap = cv2.VideoCapture(fullpath)
            input_frames = Capture(cap, s, e)

            basename, _ = os.path.splitext(filename)
            outname = "{basename}_{scene}.avi".format(basename=basename, scene=i)
            outpath = os.path.join(video_root, outname)
            w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            out = cv2.VideoWriter(outpath,
                                  cv2.VideoWriter_fourcc(*'MJPG'),
                                  fps,
                                  (int(w), int(h)))

            for frame in input_frames.frames():
                out.write(frame)
                total_frames += 1

            out.release()
            cap.release()
            outfiles.append(outname)
            yield outname
            print "extracted scene ", i, s, e

        realtime_end = time()

        print "realtime fps: ", fps
        print "copying fps: ", float(total_frames)/(realtime_end-realtime_start)


    def extract_scenes(self, filename, scene_bounds):
        assert self._gen is None, "Didn't get all frames"
        self._gen = self._generator(filename, scene_bounds)
