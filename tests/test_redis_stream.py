import json
from unittest.mock import patch

import pytest

from src import streams


@pytest.mark.asyncio
async def test_send_message_to_backend(redis_client):
    await streams.send_data_to_backend_service({"message": "test_message"})
    redis_client.xadd.assert_called_once_with(
        streams.names.BACKEND_STREAM_NAME, {"message": "test_message"}
    )


@pytest.mark.asyncio
async def test_request_devices_from_backend(redis_client):
    await streams.request_devices_from_backend()
    redis_client.xadd.assert_called_once_with(
        streams.names.BACKEND_STREAM_NAME,
        json.loads('{"action": "request_all_device_data"}'),
    )


@pytest.mark.asyncio
async def test_handle_stream_message():
    with patch(
        "src.streams.send_recv.ConnectionsManager.broadcast_to_clients"
    ) as broadcast_to_clients:
        await streams.handle_stream_message(
            {"message": '[{"mqtt_id": 123,"device_type_name": "example_device_type"}]'}
        )
        broadcast_to_clients.assert_called_once_with(
            [
                {
                    "mqtt_id": 123,
                    "device_type_name": "example_device_type",
                }
            ]
        )
