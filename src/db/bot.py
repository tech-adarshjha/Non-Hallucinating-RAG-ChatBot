from config.bot import BASE_KB_PATH, getFilePath
from functools import cache
from util.dict import dotdict
from util.exception import BotNotFoundException


@cache
def getKbFiles(id):
    # mock data for now
    if id == "candawills":
        return [getFilePath(id, "Canadawills.csv")]
    else:
        raise BotNotFoundException("Bot `{0}` is not registered.".format(id))
