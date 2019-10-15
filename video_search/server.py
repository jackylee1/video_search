#!/usr/bin/env python

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Resource, Api
from video_search.config import ui_root
from video_search.videoapis import VideoApis
from video_search.guniapp import VideoSearchGuniapp
from video_search.rest import api

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_folder=ui_root, static_url_path='')
cors = CORS(app)
api.init_app(app)


@app.route('/')
@app.route('/search/<int:video_idx>/')
@app.route('/clothlookup/<int:video_idx>/')
@app.route('/investigate/<int:video_idx>/')
def send_root(video_idx=None):
    return app.send_static_file('index.html')


@app.route('/search/<string:video_idx>/video.webm')
def send_video(video_idx):
    api = VideoApis.get_api_for(video_idx)
    if api:
        return send_from_directory(api.cfg.data_folder, api.cfg.video_file)
    else:
        return 'notfound', 404


@app.route('/search/<string:video_idx>/thumbnail/<path:timesec>')
def get_thumbnail(video_idx, timesec):
    api = VideoApis.get_api_for(video_idx)
    if api:
        return send_from_directory(api.cfg.thumb_folder,
                                   api.tn.thumbnail_at(timesec))
    else:
        return 'notfound', 404


def guni_server():
    options = {
        'bind': '%s:%s' % ('127.0.0.1', '5000'),
        'workers': number_of_workers(),
        'timeout': 120,
        'access-logfile': './access.log',
        'error-logfile': './error.log'
    }
    VideoApis.load_demo_apis()
    guni_app = VideoSearchGuniapp(app, options)
    guni_app.run()


def main():
    VideoApis.load_demo_apis()
    app.run(host='0.0.0.0', port='5000', debug=True)


if __name__ == '__main__':
    # guni_server()
    main()
