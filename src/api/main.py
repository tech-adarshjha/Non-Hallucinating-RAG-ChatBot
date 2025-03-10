from fastapi import FastAPI
from api.bot import botRouter
from kb.kb import KnowledgeBase

""" kb = KnowledgeBase("candawills", "url", "https://www.canadawills.com/",
                   "Canadawills", "Canadawills FAQs")
kb.collect()
if kb.content is not None:
    kb.save()
else:
    logger.debug("No content was collected.")
"""

# Initialize FastAPI app
app = FastAPI()
app.include_router(botRouter)
