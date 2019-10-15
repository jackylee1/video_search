import pickle
import cv2
import requests
import json


class RecognizeFace():
    def __init__(self, cfg):
        self.cfg = cfg
        self.vidcap = cv2.VideoCapture(self.cfg.video_path)
        self.vidcap.read()

        def name_gen(c):
            return ' '.join([i.capitalize() for i in c.split('_')])

        def link_gen(c):
            return 'https://en.wikipedia.org/wiki/' + '_'.join(
                [i.capitalize() for i in c.split('_')])

        def icon_gen(c):
            cast_name = '_'.join([i.capitalize() for i in c.split('_')])

            url = "https://en.wikipedia.org/w/api.php"

            querystring = {
                "action": "query",
                "titles": cast_name,
                "prop": "pageimages",
                "format": "json",
                "pithumbsize": "150",
                "formatversion": "2"
            }

            headers = {
                'authority':
                "en.wikipedia.org",
                'Cache-Control':
                "no-cache",
                'upgrade-insecure-requests':
                "1",
                'user-agent':
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                'accept':
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                'accept-encoding':
                "gzip, deflate, br",
                'accept-language':
                "en-US,en;q=0.9",
                'cookie':
                "WMF-Last-Access=08-Jul-2018; WMF-Last-Access-Global=08-Jul-2018; GeoIP=IN:KA:Bengaluru:12.98:77.58:v4",
                'Postman-Token':
                "71165ae4-95dc-4d11-b478-1de972d49b3f"
            }
            try:
                response = requests.request(
                    "GET", url, headers=headers, params=querystring)
                icon_data = json.loads(response.text)
                logo_path = icon_data['query']['pages'][0]['thumbnail'][
                    'source']
            except:
                logo_path = '/unknown-person.jpg'
            return logo_path

        def data_gen(c):
            return {
                'name': name_gen(c),
                'link': link_gen(c),
                'icon': icon_gen(c)
            }  # 'icon.png'}

        def file2time(r):
            return float(r['Files'].lstrip('time_').rstrip('.txt'))

        self.cfg.object_dataFrame['Time'] = self.cfg.object_dataFrame.apply(
            file2time, axis=1)
        actor_time = self.cfg.object_dataFrame[['Actor_Present',
                                                'Time']].copy()
        actor_time['Actor_Present'] = actor_time['Actor_Present'].apply(
            str.split)
        actor_list = set()

        def add_actors(v):
            for i in v:
                actor_list.add(i)

        actor_time['Actor_Present'].apply(add_actors)
        cast_list = list(actor_list)
        cast_names = [
            ' '.join([i.capitalize() for i in c.split('_')]) for c in cast_list
        ]
        self.cast_data_map = {c: data_gen(c) for c in cast_list}
        actor_files = self.cfg.object_dataFrame[['Actor_Present', 'Files']]
        self.time_cast = actor_time.set_index('Time').sort_index()

    def get_cast_at(self, time_stamp):
        time_f = float(time_stamp)
        closest_row_no = self.time_cast.index.get_loc(time_f, method='nearest')
        cast_list = self.time_cast.iloc[closest_row_no]['Actor_Present']
        cast_data = [self.cast_data_map[c] for c in cast_list]
        return cast_data


if __name__ == '__main__':
    rf = RecognizeFace()
    names = rf.get_cast_at(160)
    print(names)
