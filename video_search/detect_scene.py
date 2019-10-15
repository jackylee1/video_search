import skvideo.io
import skvideo.measure
import numpy as np
from itertools import chain,islice

def batch(iterable, n=1000):
    frame_chunks = []
    for (i,frame) in enumerate(iterable):
        frame_chunks.append(frame)
        if (i+1)%n == 0:
            yield (i,np.array(frame_chunks))
            frame_chunks = []
    yield (i,np.array(frame_chunks))

def get_scene_boundary(filepath):
    videodata = skvideo.io.vreader(filepath)
    videometadata = skvideo.io.ffprobe(filepath)
    frame_rate = videometadata['video']['@avg_frame_rate']
    num_frames = np.int(videometadata['video']['@nb_frames'])
    width = np.int(videometadata['video']['@width'])
    height = np.int(videometadata['video']['@height'])
    duration = np.float(videometadata['video']['@duration'])
    scene_timestamps = []
    video_shape = (num_frames,height,width,3)
    for (frame_idx,video_batch) in batch(videodata,n=256):
        scene_lum_idx = skvideo.measure.scenedet(video_batch, method='histogram', parameter1=1.0)
        result = (scene_lum_idx+frame_idx)*duration*1000/num_frames
        scene_timestamps.extend(list(result))
    return scene_timestamps

from timeit import timeit
timeit(get_scene_boundary('./love_is_love.mp4'))
# print(get_scene_boundary('./organ_donate_fixed.mp4'))
