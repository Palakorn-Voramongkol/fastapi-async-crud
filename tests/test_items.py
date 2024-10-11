import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app  # Import the FastAPI app
from app.crud import create_item, get_items, get_item_by_id, update_item, delete_item
from app.schemas import ItemCreate, ItemUpdate

@pytest.mark.asyncio
async def test_create_item_success(monkeypatch):
    # Mock the create_item function to simulate a successful creation
    async def mock_create_item(name: str, description: str):
        return {"id": 1, "name": name, "description": description}

    monkeypatch.setattr("app.crud.create_item", mock_create_item)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/items", json={"name": "Test Item", "description": "This is a test item"})
    
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Item", "description": "This is a test item"}

@pytest.mark.asyncio
async def test_create_item_failure(monkeypatch):
    # Mock the create_item function to simulate a failure
    async def mock_create_item(name: str, description: str):
        raise Exception("Create item failed")

    monkeypatch.setattr("app.crud.create_item", mock_create_item)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/items", json={"name": "Test Item", "description": "This is a test item"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to create item: Create item failed"}

@pytest.mark.asyncio
async def test_get_items_success(monkeypatch):
    # Mock the get_items function to simulate a successful return of items
    async def mock_get_items():
        return [{"id": 1, "name": "Test Item", "description": "This is a test item"}]

    monkeypatch.setattr("app.crud.get_items", mock_get_items)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items")
    
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Test Item", "description": "This is a test item"}]

@pytest.mark.asyncio
async def test_read_item_success(monkeypatch):
    # Mock the get_item_by_id function to simulate a successful read
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Test Item", "description": "This is a test item"}

    monkeypatch.setattr("app.crud.get_item_by_id", mock_get_item_by_id)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/1")
    
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Item", "description": "This is a test item"}

@pytest.mark.asyncio
async def test_read_item_failure(monkeypatch):
    # Mock the get_item_by_id function to simulate item not found
    async def mock_get_item_by_id(item_id: int):
        return None

    monkeypatch.setattr("app.crud.get_item_by_id", mock_get_item_by_id)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/1")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

@pytest.mark.asyncio
async def test_update_item_success(monkeypatch):
    # Mock the get_item_by_id and update_item functions to simulate success
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Test Item", "description": "Old description"}

    async def mock_update_item(item_id: int, name: str, description: str):
        return {"id": item_id, "name": name, "description": description}

    monkeypatch.setattr("app.crud.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.crud.update_item", mock_update_item)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "Updated Item", "description": "Updated description"})
    
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Updated Item", "description": "Updated description"}

@pytest.mark.asyncio
async def test_update_item_failure(monkeypatch):
    # Mock the get_item_by_id function to simulate item not found
    async def mock_get_item_by_id(item_id: int):
        return None

    monkeypatch.setattr("app.crud.get_item_by_id", mock_get_item_by_id)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "Updated Item", "description": "Updated description"})
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

@pytest.mark.asyncio
async def test_delete_item_success(monkeypatch):
    # Mock the get_item_by_id and delete_item functions to simulate success
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Test Item", "description": "This is a test item"}

    async def mock_delete_item(item_id: int):
        return True

    monkeypatch.setattr("app.crud.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.crud.delete_item", mock_delete_item)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/items/1")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}

@pytest.mark.asyncio
async def test_delete_item_failure(monkeypatch):
    # Mock the get_item_by_id function to simulate item not found
    async def mock_get_item_by_id(item_id: int):
        return None

    monkeypatch.setattr("app.crud.get_item_by_id", mock_get_item_by_id)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/items/1")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
