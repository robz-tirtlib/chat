import logging

from fastapi import FastAPI

from src.presentation.api.endpoints.chat.chat import chat_router


logging.basicConfig(level=logging.DEBUG)


app = FastAPI()

app.include_router(chat_router)
