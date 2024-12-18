from config.bot import BASE_KB_PATH, getFilePath
from functools import cache
from util.dict import dotdict
from util.exception import BotNotFoundException


@cache
def getKbFiles(id):
    # mock data for now
    if id == "botid":
        return [getFilePath(id, "greetings.csv"), getFilePath(id, "Expanded_Canandawills_FAQ.csv"), getFilePath(id, "Basic_Conversation_BotInfo_Canadawills.csv")]
    else:
        raise BotNotFoundException("Bot `{0}` is not registered.".format(id))
