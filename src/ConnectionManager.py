import json
import logging
import os

from fastapi import WebSocket

from src.SingletonMeta import SingletonMeta

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ConnectionManager(metaclass=SingletonMeta):
    SECRET: str = os.getenv("WEBSOCKET_SECRET", "")

    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.backend_connections: list[WebSocket] = []

    def clear_backend_connection(self):
        self.backend_connections = []

    def is_backend_connection(self, websocket: WebSocket) -> bool:
        return websocket in self.backend_connections

    def add_backend_connection(self, websocket: WebSocket, secret: str):
        logger.info(f"Adding backend connection: {websocket=}, {secret=}")
        if not ConnectionManager.is_valid_secret(secret):
            logger.error(f"Invalid secret: {secret}")
            return False
        self.backend_connections.append(websocket)
        return True

    async def send_message_to_backend(self, incoming_data_str: str):
        logger.info(f"send_message_to_backend: {incoming_data_str=}")
        if not self.backend_connections:
            logger.error("No backend connection established")
            return
        for backend_connection in self.backend_connections:
            try:
                await backend_connection.send_json(data=json.loads(incoming_data_str))
            except Exception as e:
                logger.error(f"Error sending message to backend: {e}")
                self.remove_backend_connection(backend_connection)

    def add_connection(self, websocket: WebSocket):
        self.active_connections.append(websocket)
        logger.info(f"active_connections: {self.active_connections=}")

    def remove_client_connection(self, websocket: WebSocket):
        logger.info(f"remove_client_connection")
        self.active_connections.remove(websocket)
        logger.info(f"active_connections: {self.active_connections=}")

    async def broadcast_to_clients(self, json_data: dict):
        logger.info(f"broadcast_to_clients: {json_data=}")
        for connection in self.active_connections:
            await connection.send_json(data=json_data)

    @staticmethod
    def is_valid_secret(secret: str) -> bool:
        return secret == ConnectionManager.SECRET

    async def request_all_devices_data_from_backend(self):
        logger.info(f"request_all_devices_data_from_backend")
        if not self.backend_connections:
            logger.error("No backend connection established")
            return
        data = dict(action="request_all_devices_data")
        await self.send_message_to_backend(json.dumps(data))
