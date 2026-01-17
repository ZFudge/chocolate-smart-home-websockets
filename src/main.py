import logging

from fastapi import FastAPI

from src.router import ws_router

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI()

app.include_router(ws_router)
