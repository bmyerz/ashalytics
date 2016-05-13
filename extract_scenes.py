import cv2
import os
from common import Capture
import Pyro4
import extract_scenes_compilable

video_root = "/root/data/videos/"

class ExtractScenes(object):

    def extract_scenes(self, filename, scene_bounds):
        outfiles = []
        fullpath = os.path.join(video_root, filename)

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

            out.release()
            cap.release()
            outfiles.append(outname)

        return outfiles


if __name__ == '__main__':
    daemon = Pyro4.Daemon(host='172.17.0.4', port=7771)
    uri = daemon.register(ExtractScenes)
    print "proxy\n", uri
    daemon.requestLoop()
