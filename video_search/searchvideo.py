import spacy
import collections
import ast
import time
import re
from .similaritymatch import SimilarityMatch
from .lsisearch import GensimSearch

nlp = spacy.load('en')
sm = SimilarityMatch()


class SearchVideo():
    def __init__(self, cfg):
        self.cfg = cfg
        self.gs = GensimSearch(self.cfg)

    def process(self, input_query, limit=8):
        compeleteProcessStart = time.time()
        noun_chunks = self.getNNFromInput(input_query)

        if len(noun_chunks) == 0:
            result = self.gs.get_top_answer_candidates(input_query)
        else:
            result = self.gs.get_top_answer_candidates(' '.join(noun_chunks))

        # get all ids
        ids = [l[0] for l in result]
        score_list = list()
        final_ids = list()
        captions = list()
        dictionary = {}
        for id in ids:
            caption_list_string = self.cfg.caption_dataFrame['Captions'][id]
            caption_list = ast.literal_eval(caption_list_string)
            max_score = 0.0
            for caption in caption_list:
                score = sm.symmetric_sentence_similarity(input_query, caption)
                max_score = max(score, max_score)
                if max_score < score:
                    max_score = score
            if max_score > 0.52 or max_score == 0.0:
                # score_list.append(max_score)
                final_ids.append(id)
                # captions.append(caption)
                frame_time = float(
                    re.findall(r'-?\d+\.?\d*',
                               self.cfg.caption_dataFrame['Files'][id])[0])
                dictionary[frame_time] = caption
                if len(dictionary) == limit:
                    break
        if len(final_ids) == 0:
            for id in ids:
                frame_time = float(
                    re.findall(r'-?\d+\.?\d*',
                               self.cfg.caption_dataFrame['Files'][id])[0])
                dictionary[frame_time] = caption
                if len(dictionary) == limit:
                    break
        odict = collections.OrderedDict(sorted(dictionary.items()))
        completeProcessEnd = time.time()
        return odict
        # raise gen.Return(odict)

    def getNNFromInput(self, input):
        doc = nlp(input)
        noun_chunk_list = list()
        for nn_chunk in doc.noun_chunks:
            noun_chunk_list.append(str(nn_chunk.text))
        return noun_chunk_list
