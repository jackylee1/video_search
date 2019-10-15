import os
from moviepy.editor import VideoFileClip


class FrameThumbnail(object):
    """docstring for FrameThumbnail."""

    def __init__(self, cfg):
        super(FrameThumbnail, self).__init__()
        self.cfg = cfg

    def thumbnail_at(self, frame_sec_str):
        frame_sec = float(frame_sec_str)
        frame_msec_str = str(int(frame_sec * 1000))
        thumb_name = frame_msec_str + '.png'
        thumb_path = os.path.join(self.cfg.thumb_folder, thumb_name)
        if not os.path.exists(thumb_path):
            clip = VideoFileClip(self.cfg.video_path)
            clip.save_frame(thumb_path, t=frame_sec)
        return thumb_name
