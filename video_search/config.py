import os, pandas, glob
# ======= do not touch =========
curr_dir_path = os.path.dirname(os.path.abspath(__file__))
# ======= do not touch =========
# configs start below

# ENVIRONMENT CONFIGS
assets_dir = os.path.join(curr_dir_path, 'assets')
if not os.path.isdir(assets_dir):
    os.mkdir(assets_dir)

demo_list = []


class VideoConfig(object):
    """docstring for VideoConfig."""

    def __init__(self, video_id='', video_name=''):
        super(VideoConfig, self).__init__()
        self.video_id = video_id
        self.video_name = video_name
        self.data_folder = os.path.join(assets_dir, video_id, 'data')
        self.models_dir = os.path.join(assets_dir, video_id, 'models')
        self.thumb_root = 'thumbnails'
        self.thumb_folder = os.path.join(self.data_folder, self.thumb_root)
        if not os.path.isdir(self.thumb_folder):
            os.mkdir(self.thumb_folder)
        self.video_file = self.video_name + '.webm'  #'award_winning_video.webm'
        self.video_path = os.path.join(self.data_folder, self.video_file)
        self.caption_csv = os.path.join(self.data_folder, 'captions.csv')
        self.object_csv = os.path.join(self.data_folder, 'objects.csv')
        self.object_json = os.path.join(self.data_folder, 'objects.json')
        self.fashion_json = os.path.join(self.data_folder, 'fashion_data.json')
        self.sim_model_pkl = os.path.join(self.models_dir, "sim_model.pkl")
        self.dictionary_pkl = os.path.join(self.models_dir, "dictionary.pkl")
        self.lsi_pkl = os.path.join(self.models_dir, "lsi_model.pkl")
        self.tf_idf_vectorizer_pkl = os.path.join(self.models_dir,
                                                  "tf_idf_vec.pkl")
        self.object_dataFrame = pandas.read_csv(self.object_csv)
        self.caption_dataFrame = pandas.read_csv(self.caption_csv)
        self.face_encoding = os.path.join(self.models_dir, 'enc.pickle')
        self.faceidx_pkl = os.path.join(self.models_dir, 'face_nms.index.pkl')
        self.framelookup_csv = os.path.join(self.data_folder,
                                            'faceidx_lookup.csv')

    def __repr__(self):
        return '<Config #{0} -> "{1}">'.format(self.video_id, self.video_file)


def load_demo_cfgs():
    disabled_configs = ['SAcpESN_Fk4', 'ekb67icJRJ8',
                        'b8UoC23jhPc']  #HkuKHwetV6Q
    asset_roots = [
        i for i in os.listdir(assets_dir)
        if not i.startswith('.') and i not in disabled_configs
    ]
    videos = [
        glob.glob(os.path.join(assets_dir, i, 'data', '*.webm'))
        for i in asset_roots
    ]
    video_names = [i[0].rstrip('.webm').rsplit('/')[-1] for i in videos]
    global demo_list
    demo_list = [VideoConfig(*i) for i in zip(asset_roots, video_names)]


def get_demo_cfgs():
    global demo_list
    return demo_list


ui_root = 'webui'
ui_folder = os.path.join(curr_dir_path, ui_root)
