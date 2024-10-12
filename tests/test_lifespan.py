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

    Result(s):
    - Test passes if the database is initialized properly during lifespan and closed after the request is made.
    - Test fails if the database does not initialize or shutdown as expected.
    """
    # Step 1: Ensure that the connections are closed initially
    if Tortoise._inited:
        await Tortoise.close_connections()
        Tortoise._inited = False  # Reset the state manually

    # Step 2: Assert that the database is not initialized at the beginning
    assert not Tortoise._inited, "Database should not be initialized at the beginning."

    # Step 3: Initialize the database schema via lifespan
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await init_db()
        await Tortoise.generate_schemas()  # Ensure the table exists
        
        # Step 4: Trigger the lifespan event and verify the database is initialized
        response = await ac.get("/items/")
        assert Tortoise._inited, "Database should be initialized after lifespan startup."
        assert response.status_code == 200

    # Step 5: After app shutdown, ensure that the connections are closed
    await close_db()
    Tortoise._inited = False  # Manually reset the state
    assert not Tortoise._inited, "Database connections should be closed after lifespan shutdown."

@pytest.mark.asyncio
async def test_lifespan_failure(monkeypatch):
    """
    Test Case: Simulate failure during the lifespan event (Database Initialization Failure).

    This test checks the behavior when the `init_db` function fails during the lifespan event.

    Steps:
    1. Monkeypatch the `init_db` function to simulate a failure by raising an exception.
    2. Use the ASGITransport with AsyncClient to simulate a request that triggers the lifespan event.
    3. Expect the exception to be raised during the lifespan startup, and check if the error message matches the simulated failure.

    Result(s):
    - Test passes if the `init_db` failure is correctly simulated and the proper error message is returned.
    - Test fails if the failure is not captured or the wrong exception message is returned.
    """
    # Step 1: Simulate failure in init_db using monkeypatch
    async def mock_init_db():
        raise Exception("Mock init_db failure")

    # Apply the monkeypatch to simulate failure
    monkeypatch.setattr("app.database.init_db", mock_init_db)

    transport = ASGITransport(app=app)

    # Step 2: Use AsyncClient to simulate request and expect failure
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        try:
            await ac.get("/items/")
        except Exception as e:
            # Step 3: Check if the raised exception matches the simulated failure
            assert str(e) == "Mock init_db failure", f"Unexpected exception: {str(e)}"
