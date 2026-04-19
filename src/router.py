import asyncio
import json
import logging

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from src.ConnectionsManager import ConnectionsManager as CM
from src.streams.send_recv import request_devices_from_backend

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ws_router = APIRouter()


@ws_router.websocket("/ws")
async def client_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    CM().add_connection(websocket)
    asyncio.create_task(request_devices_from_backend())

    while True:
        try:
            incoming_data_str = await websocket.receive_text()
            try:
                await CM().send_message_to_backend(incoming_data_str=incoming_data_str)
            except json.JSONDecodeError as e:
                logger.error("Error in websocket_endpoint: invalid JSON: %s" % e)
                # no need to break the loop if invalid JSON
                continue
        except WebSocketDisconnect:
            logger.info("websocket disconnected")
            CM().remove_connection(websocket=websocket)
            break
        except Exception as e:
            logger.error("Error in websocket_endpoint: %s" % e)
            CM().remove_connection(websocket=websocket)
            break
