from unittest.mock import AsyncMock, patch

import pytest

from src.ConnectionsManager import ConnectionsManager as CM


@pytest.mark.asyncio
async def test_add_connection(mock_websockets: tuple[AsyncMock, AsyncMock, AsyncMock]):
    ws_1, ws_2, ws_3 = mock_websockets
    assert CM().active_connections == []

    CM().add_connection(ws_1)
    assert CM().active_connections == [ws_1]

    CM().add_connection(ws_2)
    assert CM().active_connections == [ws_1, ws_2]

    CM().add_connection(ws_3)
    assert CM().active_connections == [ws_1, ws_2, ws_3]


@pytest.mark.asyncio
async def test_remove_connection(
    mock_websockets: tuple[AsyncMock, AsyncMock, AsyncMock],
):
    ws_1, ws_2, ws_3 = mock_websockets
    CM().active_connections = [ws_1, ws_2, ws_3]

    CM().remove_connection(ws_2)
    assert CM().active_connections == [ws_1, ws_3]

    CM().remove_connection(ws_3)
    assert CM().active_connections == [ws_1]

    CM().remove_connection(ws_1)
    assert CM().active_connections == []


@pytest.mark.asyncio
async def test_removing_unmanaged_connection_logs_error_and_returns():
    with patch("src.ConnectionsManager.logger.error") as mock_logger:
        CM().remove_connection(1)
        mock_logger.assert_called_once_with(
            "Could not remove websocket connection: 1 not found in active connections list"
        )


@pytest.mark.asyncio
async def test_broadcast_to_clients(
    mock_websockets: tuple[AsyncMock, AsyncMock, AsyncMock],
):
    ws_1, ws_2, ws_3 = mock_websockets
    CM().active_connections = [ws_1, ws_2, ws_3]

    await CM().broadcast_to_clients(json_data={"message": "test_message"})
    ws_1.send_json.assert_called_once_with(data={"message": "test_message"})
    ws_2.send_json.assert_called_once_with(data={"message": "test_message"})
    ws_3.send_json.assert_called_once_with(data={"message": "test_message"})
