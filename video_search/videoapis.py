from .searchvideo import SearchVideo
from .searchface import SearchFace
from .searchcloth import SearchCloth
from .processvideo import ProcessVideo
from .recognizeface import RecognizeFace
from .thumbnail import FrameThumbnail
from .config import get_demo_cfgs, load_demo_cfgs


class VideoApis(object):
    """docstring for AppComponents."""
    idx_api_map = {}
    process_api = ProcessVideo()

    def __init__(self, cfg):
        super(VideoApis, self).__init__()
        self.cfg = cfg
        self.sv = SearchVideo(self.cfg)
        self.sc = SearchCloth(self.cfg)
        self.sf = SearchFace(self.cfg)
        self.rf = RecognizeFace(self.cfg)
        self.tn = FrameThumbnail(self.cfg)

    def __repr__(self):
        return '(Api of {})'.format(self.cfg)

    @classmethod
    def get_api_for(cls, idx):
        if idx in cls.idx_api_map:
            return cls.idx_api_map.get(idx)
        return None

    @classmethod
    def get_video_list(cls):
        vl = []
        for (idx, api) in cls.idx_api_map.items():
            vl.append({
                'search_loc': '/search/' + idx,
                'investigate_loc': '/investigate/' + idx,
                'clothlookup_loc': '/clothlookup/' + idx,
                'videoname': api.cfg.video_name
            })
        return vl

    @classmethod
    def load_demo_apis(cls):
        load_demo_cfgs()
        for (i, cfg) in enumerate(get_demo_cfgs()):
            cls.idx_api_map[str(i)] = cls(cfg)

    @classmethod
    def process(cls, file_form, video_name, video_id):
        demo_cfg = cls.process_api.process(file_form, video_name, video_id)
        demo_idx = str(len(cls.idx_api_map))
        new_demo_api = cls(demo_cfg)
        # print('loading ', new_demo_api)
        cls.idx_api_map[demo_idx] = new_demo_api
