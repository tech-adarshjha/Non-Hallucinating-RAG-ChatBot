import os
import random
from os import path
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from config.bot import MODEL_NAME, BASE_KB_PATH, MockBotId
from core.focused.botEngine import get_bot_engine_instance

from util.logger import logger


def get_response(bot_id, query):
    bot = get_bot_engine_instance(bot_id)
    return bot.ask(query)


# API Paths
botRouter = APIRouter()


class ChatRequest(BaseModel):
    query: str


@botRouter.post("/bot/{bot_id}")
async def chat(request: ChatRequest, bot_id) -> Any:
    try:
        # Access the text field from the JSON body
        response_text = get_response(bot_id, request.query)
        return {"status": "success", "response": response_text}
    except Exception as e:
        logger.error(e)
        return {"status": "success", "response": "Sorry, I am unable to answer your query right now. Please come back later. If its urgent, you can get drop us a mail at name@mail.com. Thanks"}
