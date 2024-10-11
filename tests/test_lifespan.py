import pytest
from httpx import AsyncClient
from app.main import app
from tortoise import Tortoise
from app.database import init_db, close_db
from httpx import ASGITransport

@pytest.mark.asyncio
async def test_lifespan():
    # Ensure that the connections are closed initially
    if Tortoise._inited:
        await close_db()
        Tortoise._inited = False  # Reset the state manually
    
    assert not Tortoise._inited, "Database should not be initialized at the beginning."

    # Initialize the database schema to prevent missing table errors
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await init_db()  # Initialize the database
        await Tortoise.generate_schemas()  # Create schemas
        response = await ac.get("/items")

        # After app startup, check that the database is initialized
        assert Tortoise._inited, "Database should be initialized after lifespan startup."
        assert response.status_code == 200

    # After app shutdown, close the connections
    await close_db()
    Tortoise._inited = False  # Manually reset the state

    assert not Tortoise._inited, "Database connections should be closed after lifespan shutdown."
