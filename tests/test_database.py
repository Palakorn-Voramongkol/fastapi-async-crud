import pytest
from app.database import init_db, close_db
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_init_db():
    """
    Test Case: Initialize the database and confirm its connectivity.
    
    This test ensures that the `init_db` function initializes the database successfully 
    and that the database is usable after initialization.

    Steps:
    1. Initialize an in-memory SQLite database (`sqlite://:memory:`) using `init_db`.
    2. Attempt a simple database operation by querying all items from the `Item` model.
    3. Catch any exceptions raised during the database operation. If the operation fails,
       fail the test with the raised exception message.
    4. Close the database connection using `close_db` after the test.

    Result(s):
    - Test passes if the database is initialized successfully and the operation to query
      items from the `Item` model is successful.
    - Test fails if any exceptions occur during the initialization or operation steps.
    """
    # Step 1: Initialize the in-memory SQLite database
    await init_db(db_url='sqlite://:memory:')
    
    # Step 2: Perform a simple database operation to confirm connectivity
    from app.db.models import Item
    try:
        items = await Item.all()
    except Exception as e:
        # Step 3: Catch any exceptions and fail the test if operation fails
        pytest.fail(f"Database operation failed after initialization: {e}")
    
    # Step 4: Close the database connection
    await close_db()

@pytest.mark.asyncio
async def test_close_db():
    """
    Test Case: Close the database connections and ensure proper behavior.
    
    This test verifies that the `close_db` function correctly closes database connections 
    and that it can be called multiple times without raising errors.

    Steps:
    1. Initialize the in-memory SQLite database using `init_db`.
    2. Call `close_db` to close the database connections.
    3. Use `patch` to mock the `Tortoise.close_connections` method.
    4. Call `close_db` again and verify that the mock `close_connections` method is 
       awaited exactly once.

    Result(s):
    - Test passes if the `close_db` function behaves as expected, properly closing the 
      database connections without errors.
    - Test fails if calling `close_db` multiple times raises an error or if the mock 
      `close_connections` method is not awaited as expected.
    """
    # Step 1: Initialize the in-memory SQLite database
    await init_db(db_url='sqlite://:memory:')
    
    # Step 2: Close the database connections
    await close_db()

    # Step 3: Use patch to mock the `Tortoise.close_connections` method
    with patch('tortoise.Tortoise.close_connections', new_callable=AsyncMock) as mock_close:
        # Step 4: Call `close_db` again and verify the mock
        await close_db()
        mock_close.assert_awaited_once()
