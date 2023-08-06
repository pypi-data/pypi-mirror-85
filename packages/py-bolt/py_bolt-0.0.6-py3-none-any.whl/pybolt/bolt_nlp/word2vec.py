from gensim.models import Word2Vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Word2Vector(object):

    def __init__(self):
        self.model = None

    def get_train_data(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                yield line.split()

    def fit(self, sentence, sg=1, size=256, min_count=5, workers=16):
        self.model = Word2Vec(sentence, sg=sg, size=size, min_count=min_count, workers=workers)

    def save(self, model_name: str):
        self.model.save(model_name)
