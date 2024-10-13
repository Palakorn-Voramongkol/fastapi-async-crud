import pytest
import pytest_asyncio


from app.main import app  # Adjust based on your project structure

from app.crud.item import (
    create_item,
    get_items,
    get_item_by_id,
)
from app.schemas.item import ItemCreate
from tortoise import Tortoise
from app.utils.exceptions import ItemError


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
async def test_get_item_from_db():
    """
    Test Case: Retrieve an item from the database by its ID.
    
    This test verifies that the `get_item_by_id` function retrieves the correct item from 
    the database when given an existing item's ID.

    Steps:
    1. Create an item using `create_item`.
    2. Retrieve the item by its ID using `get_item_by_id`.
    3. Assert that the retrieved item's details match the created item.

    Result(s):
    - Test passes if the item is successfully retrieved, and its details match the created item.
    """
    # Step 1: Create an item using the ItemCreate Pydantic model
    item_data = ItemCreate(name="Get Item", description="Retrieve this item")
    created_item = await create_item(item_data)

    # Step 2: Retrieve the item by its ID
    item = await get_item_by_id(created_item.id)

    # Step 3: Verify the retrieved item details match the created item
    assert item.id == created_item.id
    assert item.name == "Get Item"
    assert item.description == "Retrieve this item"



@pytest.mark.asyncio
async def test_get_item_from_db_not_found():
    """
    Test Case: Try retrieving an item that doesn't exist in the database.
    
    This test ensures that the `get_item_by_id` function raises `ItemError` 
    if an item with the specified ID does not exist in the database.

    Steps:
    1. Attempt to retrieve an item with a non-existent ID.
    2. Assert that the function raises `ItemError`.

    Result(s):
    - Test passes if `ItemError` is raised for a non-existent item.
    """
    # Step 1: Attempt to retrieve an item with a non-existent ID and assert the exception is raised
    with pytest.raises(ItemError) as exc_info:
        await get_item_by_id(999)
    
    # Step 2: Verify that the error message includes information about the missing item
    assert "Failed to retrieve item by ID 999" in str(exc_info.value)
    assert "Item with ID 999 not found" in str(exc_info.value)




@pytest.mark.asyncio
async def test_get_items():
    """
    Test Case: Retrieve all items from the database.
    
    This test ensures that the `get_items` function correctly retrieves all items in the database.
    
    Steps:
    1. Assert that the database is empty initially.
    2. Create multiple items using `create_item`.
    3. Retrieve all items using `get_items`.
    4. Assert that the correct items are returned.

    Result(s):
    - Test passes if all created items are successfully retrieved and match the input data.
    """
    # Step 1: Verify that the database is empty initially
    items = await get_items()
    assert isinstance(items, list)
    assert len(items) == 0

    # Step 2: Create multiple items using ItemCreate Pydantic model
    item_data1 = ItemCreate(name="Item 1", description="Description 1")
    item_data2 = ItemCreate(name="Item 2", description="Description 2")
    await create_item(item_data1)
    await create_item(item_data2)

    # Step 3: Retrieve all items
    items = await get_items()

    # Step 4: Verify that the correct items are returned
    assert len(items) == 2
    item_names = [item.name for item in items]
    assert "Item 1" in item_names
    assert "Item 2" in item_names




@pytest.mark.asyncio
async def test_get_items_with_invalid_parameters():
    """
    Test Case: Attempt to retrieve items with invalid parameters.
    
    This test ensures that when invalid query parameters are provided to the 
    `get_items` function, an appropriate error is raised.
    
    Steps:
    1. Attempt to retrieve items using invalid parameters, such as a negative limit.
    2. Assert that the correct exception (ItemError) is raised.

    Result(s):
    - Test passes if an `ItemError` is raised when invalid parameters are provided.
    """
    # Step 1: Provide an invalid limit (negative value)
    invalid_limit = -10
    
    # Step 2: Attempt to retrieve items with the invalid limit and expect an error
    with pytest.raises(ItemError) as exc_info:
        await get_items(limit=invalid_limit, offset=0)
    
    # Step 3: Verify that the exception contains the expected error message
    assert "An error occurred: Failed to retrieve items: Limit should be non-negative" in str(exc_info.value)





@pytest.mark.asyncio
async def test_get_item_by_id_failure(monkeypatch):
    """
    Test Case: Simulate a database error during item retrieval by ID.
    
    This test ensures that if an error occurs during the retrieval process,
    an `ItemError` is raised.

    Steps:
    1. Monkeypatch `Item.get_or_none` to raise a simulated database error.
    2. Attempt to retrieve an item by its ID.
    3. Assert that an `ItemError` is raised with the appropriate error message.

    Result(s):
    - Test passes if `ItemError` is raised, and the error message contains the expected details.
    """
    # Step 1: Monkeypatch to simulate a database error during retrieval
    async def mock_item_get_or_none(*args, **kwargs):
        raise Exception("Database error")

    monkeypatch.setattr("app.db.models.Item.get_or_none", mock_item_get_or_none)

    # Step 2: Attempt to retrieve the item by ID and expect an `ItemError` to be raised
    with pytest.raises(ItemError) as exc_info:
        await get_item_by_id(item_id=123)

    # Step 3: Verify that the error message includes 'An error occurred: Failed to retrieve item by ID'
    assert "An error occurred: Failed to retrieve item" in str(exc_info.value)
    assert "Database error" in str(exc_info.value)

