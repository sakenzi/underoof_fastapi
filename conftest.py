import pytest
from httpx import AsyncClient


@pytest.fixture
async def httpx_client():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client