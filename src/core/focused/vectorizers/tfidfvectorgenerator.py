import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from util.exception import NotFoundException

from config.bot import getModelPath, getModelName


class TfidfVectorGenerator:

    def __init__(self, bot_id, size=100):
        self.model_dir = getModelPath(bot_id)
        self.model_file_path = getModelName(bot_id)
        self.vec_size = size
        self.vectorizer = None
        if os.path.exists(self.model_file_path):
            with open(self.model_file_path, "rb") as input_file:
                self.vectorizer = pickle.load(input_file)

    def vectorize(self, clean_questions):
        self.vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
        self.vectorizer.fit(clean_questions)
        with open(self.model_file_path, 'wb') as output_file:
            pickle.dump(self.vectorizer, output_file)

        transformed_X = []
        # Getting memory error
        if self.vectorizer:
            transformed_X_csr = self.vectorizer.transform(clean_questions)
            transformed_X = transformed_X_csr.A  # csr_matrix to numpy matrix
        return transformed_X

    def query(self, clean_usr_msg):
        t_usr_array = None
        t_usr = self.vectorizer.transform([clean_usr_msg])
        if t_usr.size == 0:
            raise NotFoundException("No matching vector found")
        t_usr_array = t_usr.toarray()

        return t_usr_array
