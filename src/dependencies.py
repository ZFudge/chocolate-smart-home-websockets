import os
from contextvars import ContextVar

from redis.asyncio import Redis


def redis_closure():
    redis_client: Redis | None = None

    def redis_client_func():
        nonlocal redis_client
        if redis_client is None:
            redis_client = Redis(host=os.getenv("REDIS_HOST"), decode_responses=True)
        yield redis_client

    return redis_client_func


get_redis = redis_closure()

redis_client: ContextVar[Redis] = ContextVar("redis_client", default=next(get_redis()))
