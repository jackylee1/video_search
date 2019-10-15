import json
import math


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


class SearchCloth(object):
    """docstring for SearchCloth."""

    def __init__(self, cfg):
        super(SearchCloth, self).__init__()
        self.cfg = cfg
        try:

            with open(self.cfg.object_json, 'r') as f:
                self.time_object_data = json.load(f)
            with open(self.cfg.fashion_json, 'r') as f:
                self.fashion_data = json.load(f)
        except Exception as e:
            print(e)

    def get_cloth_link(self, x, y, timestamp):
        try:
            distance_map = dict()
            min_distance = 1000000000
            temp_object_data = self.time_object_data[timestamp]
            for each_object in temp_object_data:
                x1, y1, x2, y2 = [
                    int(ele)
                    for ele in temp_object_data[each_object].split(' ')
                ]
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                distance = get_distance(x, y, mid_x, mid_y)
                if (distance < min_distance or distance == -1):
                    min_distance = distance
                distance_map[distance] = each_object
            return self.fashion_data[distance_map[min_distance]]
        except Exception as e:
            print(e)
            return []
