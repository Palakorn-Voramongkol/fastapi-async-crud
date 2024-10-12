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
from pydantic import ValidationError
from fastapi import status  # Import status from FastAPI
from app.db.models import Item 
from tortoise import Tortoise
from tortoise.exceptions import OperationalError
from app.schemas.item import ItemCreate, ItemUpdate
from app.crud.item import create_item, update_item

from app.api.endpoints.items import get_item_by_id, update_item  # Import necessary functions



from app.utils.exceptions import ItemNotFoundError

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
async def test_update_item_in_db():
    """
    Test Case: Update an existing item in the database.
    
    This test verifies that the `update_item` function correctly updates an item's 
    name and description in the database.

    Steps:
    1. Create an item using `create_item`.
    2. Update the item's name and description using `update_item`.
    3. Assert that the updated item matches the new data.

    Result(s):
    - Test passes if the updated item's name and description are correct.
    """
    # Step 1: Create an item using the Pydantic model
    item_data = ItemCreate(name="Old Name", description="Old Description")
    created_item = await create_item(item_data)

    # Step 2: Update the item using the Pydantic model for updates
    update_data = ItemUpdate(name="New Name", description="New Description")
    updated_item = await update_item(item_id=created_item.id, item_data=update_data)

    # Step 3: Assert that the updated item matches the new data
    assert updated_item.name == "New Name"
    assert updated_item.description == "New Description"






@pytest.mark.asyncio
async def test_update_item_name_only():
    """
    Test Case: Update only the name of an existing item in the database.
    
    This test verifies that the `update_item` function correctly updates only the 
    name field of the item without affecting the description.

    Steps:
    1. Create an item using `create_item`.
    2. Send a request to update only the name using `update_item`.
    3. Assert that the name is updated, and the description remains unchanged.

    Result(s):
    - Test passes if only the name is updated, and the description remains unchanged.
    """
    # Step 1: Create an item using the Pydantic model
    item_data = ItemCreate(name="Old Name", description="Old Description")
    created_item = await create_item(item_data)

    # Step 2: Update only the name using the ItemUpdate model
    update_data = ItemUpdate(name="New Name", description=None)  # Only updating name
    updated_item = await update_item(item_id=created_item.id, item_data=update_data)

    # Step 3: Assert that only the name is updated, and the description is unchanged
    assert updated_item.name == "New Name"
    assert updated_item.description == "Old Description"




@pytest.mark.asyncio
async def test_update_item_description_only():
    """
    Test Case: Update only the description of an existing item in the database.
    
    This test verifies that the `update_item` function correctly updates only the 
    description field of the item without affecting the name.

    Steps:
    1. Create an item using `create_item`.
    2. Send a request to update only the description using `update_item`.
    3. Assert that the description is updated, and the name remains unchanged.

    Result(s):
    - Test passes if only the description is updated, and the name remains unchanged.
    """
    # Step 1: Create an item using the Pydantic model
    item_data = ItemCreate(name="Old Name", description="Old Description")
    created_item = await create_item(item_data)

    # Step 2: Update only the description using the ItemUpdate model
    update_data = ItemUpdate(name=None, description="New Description")  # Only updating description
    updated_item = await update_item(item_id=created_item.id, item_data=update_data)

    # Step 3: Assert that only the description is updated, and the name is unchanged
    assert updated_item.name == "Old Name"
    assert updated_item.description == "New Description"




@pytest.mark.asyncio
async def test_update_item_in_db_not_found():
    """
    Test Case: Try updating an item that doesn't exist in the database.
    
    This test ensures that the `update_item` function raises `ItemNotFoundError` if an item 
    with the specified ID does not exist in the database.

    Steps:
    1. Attempt to update the non-existent item using `update_item`.
    2. Assert that the function raises `ItemNotFoundError`.

    Result(s):
    - Test passes if `ItemNotFoundError` is raised when the item is not found.
    """
    # Step 1: Attempt to update a non-existent item and expect `ItemNotFoundError` to be raised
    update_data = ItemUpdate(name="Doesn't Matter", description="Doesn't Matter")
    
    with pytest.raises(ItemNotFoundError):
        await update_item(999, update_data)




@pytest.mark.asyncio
async def test_update_item_invalid_data():
    """
    Test Case: Update an item with invalid data.
    
    This test verifies that attempting to update an item with an empty name or
    description raises a `ValidationError`.

    Steps:
    1. Create an item using `create_item`.
    2. Attempt to update the item with invalid data (empty name or description).
    3. Assert that a `ValidationError` is raised for each invalid field.

    Result(s):
    - Test passes if a `ValidationError` is raised for invalid name or description.
    """
    # Step 1: Create an item using valid data
    item_data = ItemCreate(name="Valid Name", description="Valid Description")
    created_item = await create_item(item_data)

    # Step 2: Attempt to update with an empty name
    with pytest.raises(ValidationError):
        update_data = ItemUpdate(name="", description="Valid Description")
        await update_item(created_item.id, update_data)

    # Step 3: Attempt to update with an empty description
    with pytest.raises(ValidationError):
        update_data = ItemUpdate(name="Valid Name", description="")
        await update_item(created_item.id, update_data)

'''
@pytest.mark.asyncio
async def test_update_item_database_error(monkeypatch):
    """
    Test Case: Simulate a database error during item update.
    
    This test ensures that if a database error occurs during the update, 
    an `ItemError` is raised.

    Steps:
    1. Monkeypatch the database methods to simulate an error.
    2. Attempt to update the item using `update_item`.
    3. Assert that an `ItemError` is raised with the appropriate error message.

    Result(s):
    - Test passes if `ItemError` is raised, and the error message contains the expected details.
    """
    # Step 1: Monkeypatch the database methods
    async def mock_item_get_or_none(*args, **kwargs):
        return Item(id=123, name="Old Name", description="Old Description")
    
    async def mock_item_save(*args, **kwargs):
        raise Exception("Database error")

    monkeypatch.setattr("app.db.models.Item.get_or_none", mock_item_get_or_none)
    monkeypatch.setattr("app.db.models.Item.save", mock_item_save)

    # Step 2: Prepare the update data
    update_data = ItemUpdate(name="Updated Name", description="Updated Description")

    # Step 3: Attempt to update the item and expect an `ItemError` to be raised
    with pytest.raises(ItemError) as exc_info:
        await update_item(item_id=123, item_data=update_data)
    
    # Step 4: Assert that the error message matches the expected message
    assert "An error occurred: Database error" in str(exc_info.value)
'''

@pytest.mark.asyncio
async def test_update_item_endpoint_failures(monkeypatch):
    """
    Test Case: Simulate failure scenarios in the `update_item` endpoint.

    This test ensures that the correct error codes are returned for different failure
    scenarios when updating an item via the FastAPI endpoint.

    Steps:
    1. Simulate a 404 error when the item does not exist.
    2. Simulate a 422 error for invalid data (empty name or description).
    3. Simulate a 500 error for update failure.

    Result(s):
    - Test passes if the correct status codes (404, 422, 500) and messages are returned.
    """
    # Step 1: Simulate 404 Not Found (Item doesn't exist)
    async def mock_get_item_by_id_404(id: int):
        return None

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id_404)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/items/9999", json={"name": "Updated Name", "description": "Updated Description"})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Item not found" in response.json()["detail"]

    # Step 2: Simulate 422 Unprocessable Entity (Invalid Name or Description)
    async def mock_get_item_by_id(id: int):
        return {"id": id, "name": "Existing Item", "description": "Existing Description"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    # Invalid Name
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "", "description": "Updated Description"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "value_error" in response.json()["detail"][0]["type"]

    # Invalid Description
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "Updated Name", "description": ""})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "value_error" in response.json()["detail"][0]["type"]

    # Step 3: Simulate 500 Internal Server Error (Update failure)
    async def mock_update_item(id: int, **updates):
        # Simulate a failure in the update process by raising an Exception
        raise Exception("Failed to update item")

    monkeypatch.setattr("app.api.endpoints.items.update_item", mock_update_item)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "Updated Name", "description": "Updated Description"})
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to update item" in response.json()["detail"]
