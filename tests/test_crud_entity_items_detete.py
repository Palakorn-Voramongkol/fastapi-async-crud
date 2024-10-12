import pytest
import pytest_asyncio

from httpx import AsyncClient
from app.main import app  # Adjust based on your project structure

from app.crud.item import (
    create_item,
    get_items,
    get_item_by_id,
    update_item,
    delete_item,
    ItemError
)

from app.db.models import Item 
from tortoise import Tortoise
from tortoise.exceptions import OperationalError

@pytest_asyncio.fixture(scope="function", autouse=True)
async def initialize_tests():
    """
    Fixture to initialize the Tortoise ORM for each test case.
    
    This fixture runs before each test function, initializing an in-memory SQLite database 
    and generating the necessary schemas for testing. It ensures that each test function 
    starts with a fresh, isolated database.

    Steps:
    1. **Initialize Tortoise ORM**: Sets up an in-memory SQLite database (`sqlite://:memory:`).
    2. **Generate Schemas**: Creates tables based on the models defined in `app.models`.
    3. **Yield**: Control is handed over to the test function after database initialization.
    4. **Close Connections**: Ensures that the database connections are properly closed after each test.

    This fixture ensures that tests are isolated and do not interfere with each other by 
    creating a fresh database for every test.
    """
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.db.models"]}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

@pytest.mark.asyncio
async def test_delete_item_from_db():
    """
    Test Case: Delete an existing item from the database.
    
    This test verifies that the `delete_item` function successfully deletes an 
    item from the database.

    Steps:
    1. Create an item using `create_item`.
    2. Delete the item using `delete_item`.
    3. Verify that the item no longer exists in the database using `get_item_by_id`.

    Expectation:
    - The item should be successfully deleted from the database, and `get_item_by_id` should return `None`.

    Result(s):
    - Test passes if the item is deleted, and `get_item_by_id` returns `None`.
    """
    # Step 1: Create an item
    item_data = {"name": "Delete Me", "description": "To be deleted"}
    created_item = await create_item(**item_data)

    # Step 2: Delete the item
    result = await delete_item(created_item.id)
    assert result is True

    # Step 3: Verify the item no longer exists
    item = await get_item_by_id(created_item.id)
    assert item is None

@pytest.mark.asyncio
async def test_delete_item_from_db_not_found():
    """
    Test Case: Try deleting an item that doesn't exist in the database.
    
    This test ensures that the `delete_item` function returns `False` if an item 
    with the specified ID does not exist in the database.

    Steps:
    1. Attempt to delete a non-existent item.
    2. Verify that the `delete_item` function returns `False`.

    Expectation:
    - Attempting to delete a non-existent item should return `False`.

    Result(s):
    - Test passes if `delete_item` returns `False` when the item does not exist.
    """
    # Step 1: Attempt to delete a non-existent item
    result = await delete_item(999)

    # Step 2: Verify the deletion result is False
    assert result is False

@pytest.mark.asyncio
async def test_delete_already_deleted_item():
    """
    Test Case: Attempt to delete an already deleted item.
    
    This test ensures that once an item is deleted, attempting to delete it again 
    returns the correct result (`False`).

    Steps:
    1. Create an item using `create_item`.
    2. Delete the item using `delete_item`.
    3. Attempt to delete the same item again using `delete_item`.
    4. Verify that the second deletion attempt returns `False`.

    Expectation:
    - Deleting an already deleted item should return `False`.

    Result(s):
    - Test passes if `delete_item` returns `False` on the second attempt to delete the item.
    """
    # Step 1: Create an item
    item_data = {"name": "Item to be Deleted", "description": "To be deleted"}
    created_item = await create_item(**item_data)

    # Step 2: Delete the item the first time
    result = await delete_item(created_item.id)
    assert result is True

    # Step 3: Attempt to delete the item again
    result = await delete_item(created_item.id)
    assert result is False

@pytest.mark.asyncio
async def test_delete_item_database_error(monkeypatch):
    """
    Test Case: Simulate a database error during item deletion.
    
    This test ensures that if a database error occurs during the deletion process,
    an `ItemError` is raised.

    Steps:
    1. Monkeypatch `Item.get_or_none` to return a valid item.
    2. Monkeypatch `Item.delete` to raise a simulated database error.
    3. Attempt to delete the item using `delete_item`.
    4. Verify that an `ItemError` is raised with the appropriate error message.

    Expectation:
    - A database error during item deletion should raise an `ItemError` with the correct error message.

    Result(s):
    - Test passes if `ItemError` is raised, and the error message contains the expected details.
    """
    # Step 1: Monkeypatch to return a valid item
    async def mock_item_get_or_none(*args, **kwargs):
        return Item(id=123, name="Test Item", description="Test Description")

    # Step 2: Monkeypatch to simulate a database error during deletion
    async def mock_item_delete(*args, **kwargs):
        raise Exception("Database error during deletion")

    monkeypatch.setattr("app.db.models.Item.get_or_none", mock_item_get_or_none)
    monkeypatch.setattr("app.db.models.Item.delete", mock_item_delete)

    # Step 3: Attempt to delete the item and expect an `ItemError` to be raised
    with pytest.raises(ItemError) as exc_info:
        await delete_item(item_id=123)

    # Step 4: Verify that the error message includes 'Failed to delete item'
    assert "Failed to delete item with ID 123" in str(exc_info.value)
    assert "Database error during deletion" in str(exc_info.value)
