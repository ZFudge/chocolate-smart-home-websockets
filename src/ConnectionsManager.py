import logging
from typing import List

from fastapi import WebSocket

from src.SingletonMeta import SingletonMeta

logger = logging.getLogger(__name__)


class ConnectionsManager(metaclass=SingletonMeta):
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    def add_connection(self, websocket: WebSocket):
        self.active_connections.append(websocket)

    def remove_connection(self, websocket: WebSocket):
        try:
            self.active_connections.remove(websocket)
        except ValueError:
            logger.error(
                f"Could not remove websocket connection: {websocket} not found in active connections list"
            )

    async def broadcast_to_clients(self, json_data: dict):
        for connection in self.active_connections:
            await connection.send_json(data=json_data)
