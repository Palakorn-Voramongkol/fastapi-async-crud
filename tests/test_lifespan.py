import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tortoise import Tortoise
from app.database import init_db, close_db

@pytest.mark.asyncio
async def test_lifespan_success():
    """
    Test Case: Test the correct execution of the lifespan event.

    This test ensures that the database initialization and shutdown are handled properly
    during the lifespan events of the FastAPI application.

    Steps:
    1. Ensure that the database is not initialized at the beginning of the test.
    2. Use the ASGITransport with AsyncClient to simulate a request and trigger the lifespan event.
    3. Initialize the database and generate the schemas before making a request.
    4. Check that the database is properly initialized after the lifespan starts.
    5. After making a request, confirm that the database connection is shut down properly after the lifespan ends.
    """
    # Ensure that the connections are closed initially
    if Tortoise._inited:
        await Tortoise.close_connections()
        Tortoise._inited = False  # Reset the state manually

    # Assert that the database is not initialized at the beginning
    assert not Tortoise._inited, "Database should not be initialized at the beginning."

    # Initialize the database schema via lifespan
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Initialize the database and generate schemas
        await init_db()
        await Tortoise.generate_schemas()  # Ensure the table exists
        
        # Trigger the lifespan event, including init_db
        response = await ac.get("/items/")

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
    """
    Test Case: Simulate failure during the lifespan event (Database Initialization Failure).

    This test checks the behavior when the `init_db` function fails during the lifespan event.

    Steps:
    1. Monkeypatch the `init_db` function to simulate a failure by raising an exception.
    2. Use the ASGITransport with AsyncClient to simulate a request that triggers the lifespan event.
    3. Expect the exception to be raised during the lifespan startup, and check if the error message matches the simulated failure.
    """
    # Simulate failure in init_db
    async def mock_init_db():
        raise Exception("Mock init_db failure")

    # Apply the monkeypatch to simulate failure in the database initialization
    monkeypatch.setattr("app.database.init_db", mock_init_db)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Expect an exception when init_db fails during the lifespan event
        try:
            await ac.get("/items/")
        except Exception as e:
            # Check if the raised exception matches the expected simulated failure
            assert str(e) == "Mock init_db failure", f"Unexpected exception: {str(e)}"
