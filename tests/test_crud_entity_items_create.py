import pytest
import pytest_asyncio

from httpx import AsyncClient
from app.main import app  # Adjust based on your project structure
from app.crud.item import create_item, get_items, get_item_by_id, update_item, delete_item, ItemError
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
async def test_create_item_in_db():
    """
    Test Case: Ensure item creation in database.
    
    Steps:
    1. Use `create_item` to create an item with name and description.
    2. Verify that the item's name, description, and ID are as expected.

    Expectation:
    - The item should be created successfully, and the returned item should contain the correct name, description, and a valid ID.
    
    Result(s):
    - Test passes if the item is successfully created and the name, description, and ID match the input.
    """
    # Step 1: Use create_item to create an item
    item_data = {"name": "Test Item", "description": "Test Description"}
    item = await create_item(**item_data)
    
    # Step 2: Verify the item's properties are correct
    assert item.name == "Test Item"
    assert item.description == "Test Description"
    assert isinstance(item.id, int)

@pytest.mark.asyncio
async def test_create_item_empty_name():
    """
    Test Case: Attempt to create an item with an empty name.
    
    Steps:
    1. Attempt to create an item with an empty name using `create_item`.
    2. Assert that a `ValueError` is raised.

    Expectation:
    - The `create_item` function should raise a `ValueError` for an empty name.
    
    Result(s):
    - Test passes if the `ValueError` is raised and the error message is appropriate.
    """
    # Step 1: Attempt to create an item with an empty name
    item_data = {"name": "", "description": "Test Description"}
    
    # Step 2: Assert that a ValueError is raised
    with pytest.raises(ValueError):
        await create_item(**item_data)

@pytest.mark.asyncio
async def test_create_item_empty_description():
    """
    Test Case: Attempt to create an item with an empty description.
    
    Steps:
    1. Attempt to create an item with an empty description using `create_item`.
    2. Assert that a `ValueError` is raised.

    Expectation:
    - The `create_item` function should raise a `ValueError` for an empty description.
    
    Result(s):
    - Test passes if the `ValueError` is raised and the error message is appropriate.
    """
    # Step 1: Attempt to create an item with an empty description
    item_data = {"name": "Test Item", "description": ""}
    
    # Step 2: Assert that a ValueError is raised
    with pytest.raises(ValueError):
        await create_item(**item_data)

@pytest.mark.asyncio
async def test_bulk_create_items():
    """
    Test Case: Bulk creation of items in the database.
    
    Steps:
    1. Use `create_item` to create 100 items.
    2. Retrieve all items using `get_items`.
    3. Assert that all 100 items were successfully created.

    Expectation:
    - All 100 items should be created, and each item should have a unique ID.
    
    Result(s):
    - Test passes if all 100 items are created and stored correctly in the database.
    """
    num_items = 100  # Create 100 items
    
    # Step 1: Use create_item to create multiple items
    for i in range(num_items):
        item_data = {"name": f"Item {i}", "description": f"Description {i}"}
        await create_item(**item_data)

    # Step 2: Retrieve all items and assert their count
    items = await get_items(limit=100)
    
    # Step 3: Ensure all items were created
    assert len(items) == num_items  # Ensure all items were created

@pytest.mark.asyncio
async def test_create_items_with_same_name():
    """
    Test Case: Create multiple items with the same name.
    
    Steps:
    1. Create two items with the same name but different descriptions using `create_item`.
    2. Assert that both items are created and have unique IDs.
    
    Expectation:
    - The API should allow creating multiple items with the same name, assigning each a unique ID.
    
    Result(s):
    - Test passes if both items are created and have distinct IDs.
    """
    # Step 1: Create the first item with the same name
    item_data_1 = {"name": "Same Name", "description": "Description 1"}
    item_1 = await create_item(**item_data_1)
    
    # Step 2: Create the second item with the same name
    item_data_2 = {"name": "Same Name", "description": "Description 2"}
    item_2 = await create_item(**item_data_2)
    
    # Step 3: Assert the two items have distinct IDs but the same name
    assert item_1.id != item_2.id
    assert item_1.name == item_2.name

@pytest.mark.asyncio
async def test_create_item_database_error(monkeypatch):
    """
    Test Case: Simulate a database error during item creation.
    
    Steps:
    1. Monkeypatch `Item.create` to raise an exception simulating a database error.
    2. Attempt to create an item using `create_item`.
    3. Assert that an `ItemError` is raised with the appropriate message.

    Expectation:
    - If a database error occurs, `ItemError` should be raised.

    Result(s):
    - Test passes if the `ItemError` is raised and the error message includes 'Failed to create item'.
    """
    # Step 1: Monkeypatch the create method to simulate a database error
    async def mock_item_create(*args, **kwargs):
        raise Exception("Database error")

    monkeypatch.setattr("app.db.models.Item.create", mock_item_create)

    # Step 2: Attempt to create an item and assert ItemError is raised
    with pytest.raises(ItemError) as exc_info:
        await create_item(name="name", description="Description that causes error")
    
    # Step 3: Assert the error message is appropriate
    assert "Failed to create item" in str(exc_info.value)

@pytest.mark.asyncio
async def test_create_item_with_invalid_data():
    """
    Test Case: Attempt to create an item with invalid data (empty name or description).
    
    Steps:
    1. Attempt to create an item with an empty name using `create_item`.
    2. Assert that a `ValueError` is raised.
    3. Attempt to create an item with an empty description using `create_item`.
    4. Assert that a `ValueError` is raised.
    
    Expectation:
    - The API should raise a `ValueError` for an empty name and an empty description.
    
    Result(s):
    - Test passes if `ValueError` is raised for both invalid inputs (empty name or description).
    """
    # Step 1: Attempt to create an item with an empty name
    with pytest.raises(ValueError) as exc_info_name:
        await create_item(name="", description="Valid description")
    
    # Step 2: Assert the error message for empty name is correct
    assert "Name cannot be empty" in str(exc_info_name.value)

    # Step 3: Attempt to create an item with an empty description
    with pytest.raises(ValueError) as exc_info_description:
        await create_item(name="Valid name", description="")
    
    # Step 4: Assert the error message for empty description is correct
    assert "Description cannot be empty" in str(exc_info_description.value)
