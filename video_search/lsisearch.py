import os, joblib
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer


class GensimSearch():
    lsi_model = None
    dict_lsi = None
    lsi = None

    def __init__(self, cfg):
        self.cfg = cfg
        self.load(cfg.lsi_pkl, cfg.sim_model_pkl, cfg.dictionary_pkl)

    def train(self, dataFrame):
        try:
            try:
                os.remove(self.cfg.sim_model_pkl)
                os.remove(self.cfg.dictionary_pkl)
                os.remove(self.cfg.lsi_pkl)
            except:
                pass
            print("Training Gensim LSI search Module")
            #documents_un_lemmetize = primary_classifier_data['question']
            #documents = pd.Series(map(lemmatize, documents_un_lemmetize))
            #stoplist = set(stopwords.words('english'))
            #texts = [[word for word in document.lower().split() if word not in self.stoplist] for document in self.documents]
            texts = [[word for word in document.lower().split()]
                     for document in dataFrame['Objects']]
            dictionary = gensim.corpora.Dictionary(texts)
            corp = [dictionary.doc2bow(text) for text in texts]
            topic_count = 1800
            lsi = gensim.models.lsimodel.LsiModel(
                corpus=corp,
                id2word=dictionary,
                num_topics=topic_count,
                onepass=False,
                power_iters=20)
            sim_model = gensim.similarities.MatrixSimilarity(lsi[corp])

            lsi.save(self.cfg.lsi_pkl)
            print("lsi model saved")
            sim_model.save(self.cfg.sim_model_pkl)
            print("sim model saved")
            dictionary.save(self.cfg.dictionary_pkl)
            print("lsi dictionary saved")

            # training and dumping of tf-idf
            vectorizer_word = TfidfVectorizer(
                stop_words='english', analyzer='word', ngram_range=(1, 1))
            vectorizer_word.fit(dataFrame['Objects'])
            joblib.dump(vectorizer_word, self.cfg.tf_idf_vectorizer_pkl)

            print('Models Trained......')

        except Exception as e:
            raise e

    def load(self, lsi_pkl, sim_model_pkl, dictionary_pkl):
        global tf_idf_vec_model
        try:
            self.lsi = gensim.models.lsimodel.LsiModel.load(lsi_pkl)
            self.lsi_model = gensim.similarities.MatrixSimilarity.load(
                sim_model_pkl)
            self.dict_lsi = gensim.corpora.Dictionary.load(dictionary_pkl)
            self.lsi_model.num_best = 15
        except Exception as e:
            raise e

    def get_top_answer_candidates(self, query):
        try:
            #query = lemmatize(query)
            vec_bow = self.dict_lsi.doc2bow(query.lower().split())
            vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
            # perform a similarity query against the corpus
            sims = self.lsi_model[vec_lsi]
            #sims = sorted(enumerate(sims), key=lambda x: -x[1])
            return sims
        except Exception as e:
            raise e
