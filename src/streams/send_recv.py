import asyncio
import json
import logging

import pytest

from src.ConnectionsManager import ConnectionsManager
from src.dependencies import redis_client
from src.streams.names import BACKEND_STREAM_NAME, WEBSOCKETS_STREAM_NAME

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def handle_stream_message(message: dict):
    data = json.loads(message.get("message"))
    await ConnectionsManager().broadcast_to_clients(data)


@pytest.mark.asyncio
async def handle_reads():
    last_id = "$"
    while True:
        try:
            # XREAD BLOCK 1000 STREAMS mystream $
            messages = await redis_client.get().xread(
                {WEBSOCKETS_STREAM_NAME: last_id}, count=1, block=1000
            )
            if messages:
                logger.info(f"Received messages: {messages}")
                for stream_name, message_list in messages:
                    logger.info(f"Stream name: {stream_name}")
                    for message_id, message_data in message_list:
                        logger.info(
                            f"Received message ID: {message_id}, Data: {message_data}"
                        )
                        last_id = message_id  # Update the last received ID
                        await handle_stream_message(message_data)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.exception("Error in handle_reads: %s", e)
            await asyncio.sleep(1)


@pytest.mark.asyncio
async def send_data_to_backend_service(data: dict):
    await redis_client.get().xadd(BACKEND_STREAM_NAME, data)


@pytest.mark.asyncio
async def request_devices_from_backend():
    await send_data_to_backend_service({"action": "request_all_device_data"})
