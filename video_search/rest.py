from flask import Flask, send_from_directory, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_restful import Resource, Api
from video_search.config import ui_root
from video_search.videoapis import VideoApis
from video_search.guniapp import VideoSearchGuniapp
from io import BytesIO

# set the project root directory as the static folder, you can set others.
api = Api()


class SearchVideoApi(Resource):
    def get(self, video_idx, search_text):
        api = VideoApis.get_api_for(video_idx)
        if api:
            result = api.sv.process(search_text)
            return {'results': result}
        else:
            return 'notfound', 404


class SearchFaceApi(Resource):
    def post(self, video_idx):
        search_img = BytesIO(request.data)
        api = VideoApis.get_api_for(video_idx)
        if api:
            result = api.sf.process(search_img)
            return {'results': result}
        else:
            return 'notfound', 404


class ProcessVideoApi(Resource):
    def post(self):
        file_form = request.files['file']
        filename = secure_filename(file_form.filename)
        [basename, ext] = filename.rsplit('.', 1)
        [video_name_, video_id] = basename.rsplit('-', 1)
        video_name = video_name_.rstrip('_')
        VideoApis.process(file_form, video_name, video_id)
        return {'results': 'uploaded'}


class SearchClothApi(Resource):
    def get(self, video_idx, time_stamp):
        api = VideoApis.get_api_for(video_idx)
        if api:
            x, y = int(float(request.args['x'])), int(float(request.args['y']))
            closest_cloth = api.sc.get_cloth_link(x, y,
                                                  str(int(float(time_stamp))))
            result = []
            if closest_cloth:
                result = [{'link': closest_cloth}]
            return {'results': result}
        else:
            return 'notfound', 404


class GetActorsApi(Resource):
    def get(self, video_idx, time_stamp):
        api = VideoApis.get_api_for(video_idx)
        if api:
            results = api.rf.get_cast_at(time_stamp=float(time_stamp))
            return {'results': results}
        else:
            return 'notfound', 404


class VideoListApi(Resource):
    def get(self):
        vl = VideoApis.get_video_list()
        return {'videolist': vl}


api.add_resource(SearchVideoApi,
                 '/api/search/<string:video_idx>/<string:search_text>')
api.add_resource(SearchFaceApi, '/api/investigate/<string:video_idx>/upload')
api.add_resource(SearchClothApi,
                 '/api/clothlookup/<string:video_idx>/<string:time_stamp>')
api.add_resource(ProcessVideoApi, '/api/videoprocess')
api.add_resource(GetActorsApi,
                 '/api/inspect/<string:video_idx>/<string:time_stamp>')
api.add_resource(VideoListApi, '/api/videolist')
