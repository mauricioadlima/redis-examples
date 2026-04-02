# conftest.py
import pytest
import redis

@pytest.fixture
def redis_client():
    client = redis.Redis(decode_responses=True)
    yield client
    client.flushdb()