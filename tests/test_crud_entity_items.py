import pytest
import pytest_asyncio
from app.models import Item
from app.crud.item import (
    create_item,
    get_items,
    get_item_by_id,
    update_item,
    delete_item,
)
from tortoise import Tortoise

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
        modules={"models": ["app.models"]}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

@pytest.mark.asyncio
async def test_create_item_in_db():
    """
    Test Case: Ensure that an item can be created and saved in the database.
    
    This test verifies that the `create_item` function works as expected. It ensures 
    that an item is correctly created with the specified name and description, and that 
    it is assigned an ID in the database.

    Steps:
    1. Create an item using `create_item`.
    2. Assert that the item's name, description, and ID are correct.
    """
    item_data = {"name": "Test Item", "description": "Test Description"}
    item = await create_item(**item_data)
    assert item.name == "Test Item"
    assert item.description == "Test Description"
    assert isinstance(item.id, int)

@pytest.mark.asyncio
async def test_get_item_from_db():
    """
    Test Case: Retrieve an item from the database by its ID.
    
    This test verifies that the `get_item_by_id` function retrieves the correct item from 
    the database when given an existing item's ID.

    Steps:
    1. Create an item.
    2. Retrieve the item by its ID.
    3. Assert that the retrieved item's details match the created item.
    """
    item_data = {"name": "Get Item", "description": "Retrieve this item"}
    created_item = await create_item(**item_data)

    item = await get_item_by_id(created_item.id)
    assert item.id == created_item.id
    assert item.name == "Get Item"
    assert item.description == "Retrieve this item"

@pytest.mark.asyncio
async def test_get_item_from_db_not_found():
    """
    Test Case: Try retrieving an item that doesn't exist in the database.
    
    This test ensures that the `get_item_by_id` function returns `None` if an item with 
    the specified ID does not exist in the database.

    Steps:
    1. Attempt to retrieve an item with a non-existent ID.
    2. Assert that the function returns `None`.
    """
    item = await get_item_by_id(999)
    assert item is None

@pytest.mark.asyncio
async def test_get_items():
    """
    Test Case: Retrieve all items from the database.
    
    This test ensures that the `get_items` function correctly retrieves all items in the database.
    
    Steps:
    1. Assert that the database is empty initially.
    2. Create multiple items.
    3. Retrieve all items and assert that the correct items are returned.
    """
    items = await get_items()
    assert isinstance(items, list)
    assert len(items) == 0

    item_data1 = {"name": "Item 1", "description": "Description 1"}
    item_data2 = {"name": "Item 2", "description": "Description 2"}
    await create_item(**item_data1)
    await create_item(**item_data2)

    items = await get_items()
    assert len(items) == 2
    item_names = [item.name for item in items]
    assert "Item 1" in item_names
    assert "Item 2" in item_names

@pytest.mark.asyncio
async def test_update_item_in_db():
    """
    Test Case: Update an existing item in the database.
    
    This test verifies that the `update_item` function correctly updates an item's 
    name and description in the database.

    Steps:
    1. Create an item.
    2. Update the item's name and description.
    3. Assert that the updated item matches the new data.
    """
    item_data = {"name": "Old Name", "description": "Old Description"}
    created_item = await create_item(**item_data)

    updated_item = await update_item(
        created_item.id,
        name="New Name",
        description="New Description"
    )
    assert updated_item.name == "New Name"
    assert updated_item.description == "New Description"

@pytest.mark.asyncio
async def test_update_item_name_only():
    """
    Test Case: Update only the name of an existing item in the database.
    
    This test verifies that the `update_item` function correctly updates only the 
    name field of the item without affecting the description.

    Steps:
    1. Create an item.
    2. Send a request to update only the name.
    3. Assert that the name is updated, and the description remains unchanged.
    """
    # Step 1: Create an item in the database
    item_data = {"name": "Old Name", "description": "Old Description"}
    created_item = await create_item(**item_data)

    # Step 2: Send only the name field for updating
    updated_item = await update_item(
        created_item.id,
        name="New Name"  # Only the name is sent for update
    )
    
    # Step 3: Assert that the description remains unchanged and the name is updated
    assert updated_item.name == "New Name"
    assert updated_item.description == "Old Description"  # Description should remain the same

@pytest.mark.asyncio
async def test_update_item_description_only():
    """
    Test Case: Update only the description of an existing item in the database.
    
    This test verifies that the `update_item` function correctly updates only the 
    description field of the item without affecting the name.

    Steps:
    1. Create an item.
    2. Send a request to update only the description.
    3. Assert that the description is updated, and the name remains unchanged.
    """
    # Step 1: Create an item in the database
    item_data = {"name": "Old Name", "description": "Old Description"}
    created_item = await create_item(**item_data)

    # Step 2: Send only the description field for updating
    updated_item = await update_item(
        created_item.id,
        description="New Description"  # Only the description is sent for update
    )
    
    # Step 3: Assert that the name remains unchanged and the description is updated
    assert updated_item.name == "Old Name"  # Name should remain the same
    assert updated_item.description == "New Description"



@pytest.mark.asyncio
async def test_update_item_in_db_not_found():
    """
    Test Case: Try updating an item that doesn't exist in the database.
    
    This test ensures that the `update_item` function returns `None` if an item 
    with the specified ID does not exist in the database.

    Steps:
    1. Assert that the item does not exist.
    2. Attempt to update the non-existent item.
    3. Assert that the update operation returns `None`.
    """
    item = await get_item_by_id(999)
    assert item is None

    updated_item = await update_item(
        999,
        name="Doesn't Matter",
        description="Doesn't Matter"
    )
    assert updated_item is None

@pytest.mark.asyncio
async def test_delete_item_from_db():
    """
    Test Case: Delete an existing item from the database.
    
    This test verifies that the `delete_item` function successfully deletes an 
    item from the database.

    Steps:
    1. Create an item.
    2. Delete the item.
    3. Assert that the item no longer exists in the database.
    """
    item_data = {"name": "Delete Me", "description": "To be deleted"}
    created_item = await create_item(**item_data)

    result = await delete_item(created_item.id)
    assert result is True

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
    2. Assert that the deletion operation returns `False`.
    """
    result = await delete_item(999)
    assert result is False
