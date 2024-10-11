import pytest
import pytest_asyncio
from app.database import init_db, close_db
from tortoise.exceptions import OperationalError, ConfigurationError
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_init_db():
    """
    Test Case: Initialize the database and confirm its connectivity.
    
    This test ensures that the `init_db` function initializes the database successfully 
    and that the database is usable after initialization.

    Steps:
    1. Initialize an in-memory SQLite database (`sqlite://:memory:`).
    2. Attempt a simple database operation by querying all items in the `Item` model.
    3. Catch any exceptions raised during the database operation, and fail the test 
       if the operation does not succeed.
    4. Close the database connection after the test.

    This test ensures that the `init_db` function works correctly, allowing subsequent
    operations on the database.
    """
    await init_db(db_url='sqlite://:memory:')
    
    # Perform a simple database operation to confirm connectivity
    from app.models import Item
    try:
        items = await Item.all()
    except Exception as e:
        pytest.fail(f"Database operation failed after initialization: {e}")
    
    await close_db()

@pytest.mark.asyncio
async def test_close_db():
    """
    Test Case: Close the database connections and ensure proper behavior.
    
    This test verifies that the `close_db` function correctly closes database connections 
    and that the function can be called multiple times without raising errors.

    Steps:
    1. Initialize the in-memory SQLite database.
    2. Call `close_db` to close the database connections.
    3. Use the `patch` method to mock the `Tortoise.close_connections` method and verify 
       that it is called when `close_db` is invoked.
    4. Assert that `close_connections` is awaited exactly once.
    
    This test ensures that the `close_db` function is behaving as expected, including 
    properly closing connections when called.
    """
    await init_db(db_url='sqlite://:memory:')
    await close_db()

    # Use mocking to confirm that close_connections() is called
    with patch('tortoise.Tortoise.close_connections', new_callable=AsyncMock) as mock_close:
        await close_db()
        mock_close.assert_awaited_once()
