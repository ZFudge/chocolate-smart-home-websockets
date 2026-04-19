from contextvars import ContextVar
from unittest.mock import AsyncMock

import pytest
from fastapi import WebSocket
from redis.asyncio import Redis

from src.dependencies import get_redis, redis_client as redis_client_ctx
from src.ws_app import app
from src.SingletonMeta import SingletonMeta


@pytest.fixture(scope="function", autouse=True)
def singleton_instance_cleanup():
    SingletonMeta._SINGLETONS = {}
    yield


@pytest.fixture
def mock_websockets() -> tuple[AsyncMock, AsyncMock, AsyncMock]:
    mock_ws_1 = AsyncMock(spec=WebSocket)
    mock_ws_2 = AsyncMock(spec=WebSocket)
    mock_ws_3 = AsyncMock(spec=WebSocket)
    yield (mock_ws_1, mock_ws_2, mock_ws_3)
    del mock_ws_1, mock_ws_2, mock_ws_3


def redis_closure():
    redis_client: Redis | None = None

    def redis_client_func():
        nonlocal redis_client
        if redis_client is None:
            redis_client = AsyncMock(spec=Redis)
            redis_client.xadd = AsyncMock()

        yield redis_client

    return redis_client_func


@pytest.fixture
def redis_client():
    override_get_redis = redis_closure()
    app.dependency_overrides[get_redis] = override_get_redis

    override_redis_client: ContextVar[Redis] = ContextVar(
        "redis_client", default=next(override_get_redis())
    )

    redis_client_ctx.set(next(override_get_redis()))
    app.dependency_overrides[redis_client_ctx] = override_redis_client

    yield redis_client_ctx.get()
