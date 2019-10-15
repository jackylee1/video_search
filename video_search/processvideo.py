import os
import shutil
curr_dir_path = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(curr_dir_path, 'assets')
import random, string
from .config import VideoConfig


def random_video_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=11))


class ProcessVideo(object):
    """docstring for ProcessVideo."""

    def __init__(self):
        super(ProcessVideo, self).__init__()

    def process(self, file_form, video_name, video_id):
        # print('processing video ', video_id)
        src_meta = os.path.join(assets_dir, 'b8UoC23jhPc')
        dst_meta = os.path.join(assets_dir, video_id)
        if not os.path.isdir(dst_meta):
            shutil.copytree(src_meta, dst_meta)
            cfg = VideoConfig(video_id, 'love_is_love')
            os.unlink(cfg.video_path)
        new_cfg = VideoConfig(video_id, video_name)
        file_form.save(new_cfg.video_path)
        # print('processed cfg:', new_cfg)
        return new_cfg
