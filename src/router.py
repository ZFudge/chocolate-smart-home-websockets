import asyncio
import json
import logging

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from src.ConnectionManager import ConnectionManager as CM

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ws_router = APIRouter()


@ws_router.websocket("/ws")
async def client_websocket_endpoint(websocket: WebSocket):
    logger.info(f"Received client connection")
    await websocket.accept()
    CM().add_connection(websocket)
    asyncio.create_task(CM().request_all_devices_data_from_backend())

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
            CM().remove_client_connection(websocket=websocket)
            break
        except Exception as e:
            logger.error("Error in websocket_endpoint: %s" % e)
            CM().remove_client_connection(websocket=websocket)
            break

@ws_router.websocket("/ws/{secret}")
async def backend_websocket_endpoint(backend_websocket: WebSocket, secret: str | None = None):
    logger.info(f"incoming connection: {secret=}")
    if secret is None or not CM().is_valid_secret(secret):
        logger.error(f"Invalid secret: {secret=}")
        return

    await backend_websocket.accept()
    logger.info("Received backend connection")
    CM().add_backend_connection(websocket=backend_websocket, secret=secret)
    while True:
        try:
            incoming_data_str = await backend_websocket.receive_text()
            json_data = json.loads(incoming_data_str)
            asyncio.create_task(CM().broadcast_to_clients(json_data))
        except WebSocketDisconnect:
            logger.info("backend websocket disconnected")
            CM().clear_backend_connection()
            break
        except Exception as e:
            logger.error("Error in backend websocket_endpoint: %s" % e)
            CM().clear_backend_connection()
            break
