import os
from os import path

# base folders
cwd = os.getcwd()
BASE_KB_PATH = path.join(cwd, "assets/kb_data")
MODEL_NAME = "tfidf"

# mock bot, later implement
MockBotId = "botid"


def getFilePath(botId, filename):
    return path.join(BASE_KB_PATH, botId, "files", filename)


def getModelPath(botId):
    return path.join(BASE_KB_PATH, botId)


def getModelName(botId):
    return path.join(getModelPath(botId), "_".join([botId, 'tfidf.pkl']))


def getKBPath(botId):
    return path.join(getModelPath(botId), "_".join([botId, 'kb.feather']))


def initBot(botId):
    bot_folder = getModelPath(botId)
    if not os.path.exists(bot_folder):
        os.makedirs(bot_folder)
