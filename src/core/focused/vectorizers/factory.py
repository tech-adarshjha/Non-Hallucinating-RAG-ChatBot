import os
from core.focused.vectorizers.tfidfvectorgenerator import TfidfVectorGenerator


def get_vectoriser(model_name, bot_id):
    vectoriser = None
    if model_name == "tfidf":
        vectoriser = TfidfVectorGenerator(bot_id)

    return vectoriser
