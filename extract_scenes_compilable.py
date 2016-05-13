
def extract_scenes_compilable(filename, scene_bounds)
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
