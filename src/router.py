import asyncio
import json
import logging

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from src.ConnectionsManager import ConnectionsManager as CM
from src.streams.send_recv import (
    request_devices_from_backend,
    send_data_to_backend_service,
)

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
                data = json.loads(incoming_data_str)
                if isinstance(data["mqtt_id"], list):
                    # Redis demands lists be cast to a different type.
                    # Converted back to list[int] on backend after read from redis stream.
                    data["mqtt_id"] = str(data["mqtt_id"])
                if isinstance(data["value"], (bool, list)):
                    # Redis demands bools and lists be cast to a different type.
                    # Converted back to bool/list on backend after read from redis stream.
                    # To properly load list[str} single quotes should be replaced with double-quotes
                    data["value"] = str(data["value"]).replace("'", '"')
                logger.info(f"Sending data to backend service: {data}")
                await send_data_to_backend_service(data)
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
