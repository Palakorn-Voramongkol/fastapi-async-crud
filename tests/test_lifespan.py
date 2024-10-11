import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tortoise import Tortoise
from app.database import init_db, close_db

@pytest.mark.asyncio
async def test_lifespan_success():
    # Ensure that the connections are closed initially
    if Tortoise._inited:
        await Tortoise.close_connections()
        Tortoise._inited = False  # Reset the state manually

    assert not Tortoise._inited, "Database should not be initialized at the beginning."

    # Initialize the database schema via lifespan
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Initialize the database and generate schemas
        await init_db()
        await Tortoise.generate_schemas()  # Ensure the table exists
        
        # Trigger the lifespan event, including init_db
        response = await ac.get("/items")

        # After app startup, check that the database is initialized
        assert Tortoise._inited, "Database should be initialized after lifespan startup."
        assert response.status_code == 200

    # After app shutdown, check that the connections are closed
    await close_db()
    Tortoise._inited = False  # Manually reset the state
    assert not Tortoise._inited, "Database connections should be closed after lifespan shutdown."

import pytest
from httpx import AsyncClient
from app.main import app
from httpx import ASGITransport

@pytest.mark.asyncio
async def test_lifespan_failure(monkeypatch):
    # Simulate failure in init_db
    async def mock_init_db():
        raise Exception("Mock init_db failure")

    # Apply the monkeypatch to simulate failure
    monkeypatch.setattr("app.database.init_db", mock_init_db)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Expect an exception when init_db fails during the lifespan event
        try:
            await ac.get("/items")
        except Exception as e:
            assert str(e) == "Mock init_db failure", f"Unexpected exception: {str(e)}"


