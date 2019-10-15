from face_recognition import face_encodings, load_image_file, face_locations
import os
import pandas as pd
import numpy as np
try:
    import cPickle as pickle
except:
    import pickle
import nmslib
from ast import literal_eval
from itertools import takewhile


class FaceIndex(object):
    """docstring for FaceIndex."""

    def __init__(self, cfg):
        super(FaceIndex, self).__init__()
        self.cfg = cfg
        # self.create_encodings()
        # self.create_index()
        self.load()

    def load(self):
        self.index = nmslib.init(method='hnsw', space='l2')
        self.index.loadIndex(self.cfg.faceidx_pkl)
        self.lookup_frame = pd.read_csv(self.cfg.framelookup_csv, index_col=0)

    def get_face_frames(self, face_enc):
        # face_enc = np.random.random((128, 1))
        (idx_list, dist_list) = self.index.knnQuery(face_enc, 10)
        frames_dists = takewhile(lambda x: x[1] < 0.3, zip(
            idx_list, dist_list))
        frames = [x[0] for x in frames_dists]
        return self.lookup_frame.iloc[frames]['FrameTime'].tolist()

    def create_index(self):
        encoding_df = pd.read_csv(self.cfg.object_csv)
        load_enc_pkl = lambda x: pickle.loads(literal_eval(x))
        encoding_df.loc[:, 'Face_Encodings'] = encoding_df[
            'Face_Encodings'].apply(load_enc_pkl)
        encoding_arr = []
        orig_idx = []
        for (i, v) in encoding_df['Face_Encodings'].iteritems():
            for e in v:
                orig_idx.append(i)
                encoding_arr.append(e)

        def file2time(r):
            return float(r['Files'].lstrip('time_').rstrip('.txt'))

        def lookup_frame(idx):
            return file2time(encoding_df.iloc[idx])

        idx_time_map = [lookup_frame(i) for i in orig_idx]
        face_enc_data = np.array(encoding_arr).astype(np.float32)

        # initialize a new index, using a HNSW index on Cosine Similarity
        # index = nmslib.init(method='hnsw', space='cosinesimil')
        index = nmslib.init(method='hnsw', space='l2')
        index.addDataPointBatch(face_enc_data)
        index.createIndex({'post': 2}, print_progress=True)
        index.saveIndex(self.cfg.faceidx_pkl)
        pd.DataFrame({
            'FrameTime': idx_time_map
        }).to_csv(self.cfg.framelookup_csv)

    def create_encodings(self):
        import cv2
        from tqdm import tqdm
        video_df = pd.read_csv(self.cfg.object_csv)
        video_df['Face_Encodings'] = [[]] * len(video_df.index)
        vidcap = cv2.VideoCapture(self.cfg.video_path)

        time = 0
        time_interval = 500
        vidcap.set(cv2.CAP_PROP_POS_MSEC, time)
        success = True
        success, im = vidcap.read()
        count = 0
        success = True

        vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        duration = vidcap.get(cv2.CAP_PROP_POS_MSEC)
        vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

        pbar = tqdm(total=duration)
        while success:
            mark = time / 1000.0
            file_name = 'time_' + str(mark) + '.txt'
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            fr_im = im[:, :, ::-1]
            locations = face_locations(fr_im)
            if len(locations) > 0:
                encodings = face_encodings(fr_im)
                frame_list = video_df[video_df['Files'] == file_name]
                if len(frame_list.index) > 0:
                    video_df.loc[frame_list.index, 'Face_Encodings'] = [
                        encodings
                    ] * len(frame_list.index)
            pbar.update(time_interval)
            time = time + time_interval
            vidcap.set(cv2.CAP_PROP_POS_MSEC, time)
            success, im = vidcap.read()
            count = count + 1
        stringarr = lambda x: pickle.dumps(np.array(x))
        video_df.loc[:, 'Face_Encodings'] = video_df['Face_Encodings'].apply(
            stringarr)
        video_df.to_csv(self.cfg.object_csv, index=False)


class SearchFace(object):
    """docstring for SearchFace."""

    def __init__(self, cfg):
        super(SearchFace, self).__init__()
        self.cfg = cfg
        self.fi = FaceIndex(self.cfg)

    def process(self, input_img, limit=8):
        image_data = load_image_file(input_img)
        face_list = face_locations(image_data)
        if len(face_list) > 0:
            encoding_list = face_encodings(image_data)
            results = self.fi.get_face_frames(encoding_list[0])[:limit]
            return sorted(results)
        else:
            return []
