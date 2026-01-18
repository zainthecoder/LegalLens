
import pytest
from httpx import AsyncClient, ASGITransport as HTTPX_TRANSPORT
from asgi_lifespan import LifespanManager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from main import app
from models import User, Plan, ChatSession

import asyncio

@pytest.fixture(scope="function")
async def db_client(monkeypatch):
    # Set test database name
    monkeypatch.setenv("DATABASE_NAME", "legal_lens_test")
    
    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        pytest.skip("MONGODB_URL not set", allow_module_level=True)
        
    client = AsyncIOMotorClient(mongodb_url)
    
    # Initialize beanie with test DB
    await init_beanie(database=client.get_database("legal_lens_test"), document_models=[User, Plan, ChatSession])
    
    yield client
    
    # Cleanup after test
    await client.drop_database("legal_lens_test")
    client.close()

@pytest.fixture(scope="function")
async def client(db_client):
    from main import app
    from unittest.mock import MagicMock, patch
    
    # Mock lifespan components to prevent double initialization
    # We want the app to skip init_db and init_beanie because db_client fixture already did it
    
    async def mock_startup():
        return db_client
        
    async def mock_init_beanie(*args, **kwargs):
        pass

    # Patch modules in main.py namespace
    with patch("main.init_db", side_effect=mock_startup), \
         patch("main.init_beanie", side_effect=mock_init_beanie):
         
        async with LifespanManager(app):
            async with AsyncClient(transport=HTTPX_TRANSPORT(app=app), base_url="http://test") as ac:
                yield ac
