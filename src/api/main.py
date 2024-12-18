from fastapi import FastAPI
from api.bot import botRouter

# Initialize FastAPI app
app = FastAPI()
app.include_router(botRouter)
