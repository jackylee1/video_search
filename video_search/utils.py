from __future__ import unicode_literals
import youtube_dl


def download_youtube(yt_url, path, name):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])
