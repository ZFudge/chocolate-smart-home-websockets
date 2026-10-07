import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.router import ws_router
from src.streams.send_recv import handle_reads

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.include_router(ws_router)
    asyncio.create_task(handle_reads())
    yield


app = FastAPI(lifespan=lifespan)
