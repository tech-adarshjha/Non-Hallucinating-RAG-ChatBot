import os
import csv
import faiss
import nltk
import numpy as np
import pandas as pd
from nltk.stem.lancaster import LancasterStemmer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split as tts
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.svm import SVC
from core.focused.vectorizers.factory import get_vectoriser
from util.logger import logger
from pathlib import Path
from functools import lru_cache

from config.bot import MODEL_NAME, getModelPath, getKBPath
from db.bot import getKbFiles

""" nltk.download('punkt_tab')
"""


class BotEngine:
    def __init__(self, id):

        self.botId = id
        self.vector_store = None
        self.stemmer = LancasterStemmer()
        self.le = LE()
        self.classifier = None
        self.build_model(MODEL_NAME)

    def cleanup(self, sentence):
        word_tok = nltk.word_tokenize(sentence)
        stemmed_words = [self.stemmer.stem(w) for w in word_tok]
        return ' '.join(stemmed_words)

    def build_model(self, type, reset=False):
        self.vectorizer = get_vectoriser(type, self.botId)

        # Knowledge Base
        kb = Path(getKBPath(self.botId))
        if kb.is_file() and not reset:
            self.data = pd.read_feather(kb.resolve())

        else:
            kb_files = getKbFiles(self.botId)
            dataframeslist = [pd.read_csv(csvfile, encoding="utf-8", quotechar='"').dropna()
                              for csvfile in kb_files]
            df = pd.concat(dataframeslist, ignore_index=True)
            # write df to json file
            # df.to_json("./x.json", orient='records', lines=True)

            df['Clean_Question'] = df['Question'].apply(
                lambda x: self.cleanup(x))
            df['Question_embeddings'] = list(
                self.vectorizer.vectorize(df['Clean_Question'].tolist()))
            self.data = df
            df.to_feather(kb.resolve())

        self.questions = self.data['Question'].values
        X = self.data['Question_embeddings'].tolist()

        X = np.array(X)
        d = X.shape[1]
        index = faiss.IndexFlatL2(d)
        if index.is_trained:
            index.add(X)
        self.vector_store = index

        if 'Class' not in list(self.data.columns):
            return

        y = self.data['Class'].values.tolist()

        if len(set(y)) < 2:  # 0 or 1
            return

        y = self.le.fit_transform(y)

        trainx, testx, trainy, testy = tts(
            X, y, test_size=.25, random_state=42)

        self.classifier = SVC(kernel='linear')
        self.classifier.fit(trainx, trainy)

    # @lru_cache(maxsize=4096)
    def ask(self, usr):
        try:
            cleaned_usr = self.cleanup(usr)
            t_usr_array = self.vectorizer.query(cleaned_usr)
            if self.classifier:
                prediction = self.classifier.predict(t_usr_array)[0]
                class_ = self.le.inverse_transform([prediction])[0]
                questionset = self.data[self.data['Class'] == class_]
            else:
                questionset = self.data

            top_k = 1
            D, I = self.vector_store.search(t_usr_array, top_k)
            threshold = D[0][0]
            logger.info("Threshold : {0}".format(threshold))
            if threshold > 0.7:
                question_index = int(I[0][0])
                return self.data['Answer'][question_index]
            else:
                return "Sorry, I can't answer that."

        except Exception as e:
            logger.error(e)
            return "Sorry, I can't answer that."

# Function to get or create a BotEngine instance


@lru_cache(maxsize=1024)
def get_bot_engine_instance(bot_id):
    return BotEngine(bot_id)
