import pytest
from httpx import AsyncClient
from databases import Database
from model.models import Base


DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASS = "saken2020"
DB_NAME = "findroof"
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

@pytest.fixture
async def httpx_client():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client

@pytest.fixture
async def test_db():
    database = Database(DATABASE_URL)
    await database.connect()

    await database.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")

    yield database
    await database.disconnect()