# tests/test_crud.py

import pytest
import pytest_asyncio
from app.models import Item
from app.crud import (
    create_item,
    get_items,
    get_item_by_id,
    update_item,
    delete_item,
)
from tortoise import Tortoise

@pytest_asyncio.fixture(scope="function", autouse=True)
async def initialize_tests():
    # Initialize Tortoise ORM with in-memory SQLite database
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.models"]}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

@pytest.mark.asyncio
async def test_create_item_in_db():
    item_data = {"name": "Test Item", "description": "Test Description"}
    item = await create_item(**item_data)
    assert item.name == "Test Item"
    assert item.description == "Test Description"
    assert isinstance(item.id, int)

@pytest.mark.asyncio
async def test_get_item_from_db():
    # Create an item to retrieve
    item_data = {"name": "Get Item", "description": "Retrieve this item"}
    created_item = await create_item(**item_data)

    # Retrieve the item
    item = await get_item_by_id(created_item.id)
    assert item.id == created_item.id
    assert item.name == "Get Item"
    assert item.description == "Retrieve this item"

@pytest.mark.asyncio
async def test_get_item_from_db_not_found():
    item = await get_item_by_id(999)
    assert item is None

@pytest.mark.asyncio
async def test_get_items():
    # Ensure the database is empty initially
    items = await get_items()
    assert isinstance(items, list)
    assert len(items) == 0

    # Create some items
    item_data1 = {"name": "Item 1", "description": "Description 1"}
    item_data2 = {"name": "Item 2", "description": "Description 2"}
    await create_item(**item_data1)
    await create_item(**item_data2)

    # Retrieve all items
    items = await get_items()
    assert len(items) == 2
    item_names = [item.name for item in items]
    assert "Item 1" in item_names
    assert "Item 2" in item_names

@pytest.mark.asyncio
async def test_update_item_in_db():
    # Create an item to update
    item_data = {"name": "Old Name", "description": "Old Description"}
    created_item = await create_item(**item_data)

    # Update the item
    updated_item = await update_item(
        created_item.id,
        name="New Name",
        description="New Description"
    )
    assert updated_item.name == "New Name"
    assert updated_item.description == "New Description"

@pytest.mark.asyncio
async def test_update_item_in_db_not_found():
    # Ensure the item does not exist
    item = await get_item_by_id(999)
    assert item is None

    # Attempt to update the non-existent item
    updated_item = await update_item(
        999,
        name="Doesn't Matter",
        description="Doesn't Matter"
    )
    assert updated_item is None

@pytest.mark.asyncio
async def test_delete_item_from_db():
    # Create an item to delete
    item_data = {"name": "Delete Me", "description": "To be deleted"}
    created_item = await create_item(**item_data)

    # Delete the item
    result = await delete_item(created_item.id)
    assert result is True

    # Verify deletion
    item = await get_item_by_id(created_item.id)
    assert item is None

@pytest.mark.asyncio
async def test_delete_item_from_db_not_found():
    result = await delete_item(999)
    assert result is False
