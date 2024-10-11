import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Import the FastAPI app

@pytest.mark.asyncio
async def test_create_item_success(monkeypatch):
    # Mock the create_item function to simulate a successful creation
    async def mock_create_item(name: str, description: str):
        return {"id": 1, "name": name, "description": description}

    # Monkeypatch the function as it's imported in app.main
    monkeypatch.setattr("app.main.create_item", mock_create_item)

    # Use ASGITransport with AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items", json={"name": "Test Item", "description": "This is a test item"})

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item"
    
pytest.mark.asyncio
async def test_create_item_failure(monkeypatch):
    # Mock the create_item function to simulate an exception
    async def mock_create_item(name: str, description: str):
        raise Exception("Simulated exception")

    # Monkeypatch the function as it's imported in app.main
    monkeypatch.setattr("app.main.create_item", mock_create_item)

    # Use ASGITransport with AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items", json={"name": "Test Item", "description": "This is a test item"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to create item: Simulated exception"}


@pytest.mark.asyncio
async def test_read_item_success(monkeypatch):
    # Mock the get_item_by_id function to simulate a successful read
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Test Item", "description": "This is a test item"}

    monkeypatch.setattr("app.main.get_item_by_id", mock_get_item_by_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/items/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Test Item",
        "description": "This is a test item"
    }

@pytest.mark.asyncio
async def test_read_item_failure(monkeypatch):
    # Mock the get_item_by_id function to simulate item not found
    async def mock_get_item_by_id(item_id: int):
        return None  # Simulate item not found

    monkeypatch.setattr("app.main.get_item_by_id", mock_get_item_by_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/items/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

@pytest.mark.asyncio
async def test_update_item_success(monkeypatch):
    # Mock the get_item_by_id and update_item functions
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    async def mock_update_item(item_id: int, name: str, description: str):
        return {"id": item_id, "name": name, "description": description}

    monkeypatch.setattr("app.main.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.main.update_item", mock_update_item)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={
            "name": "Updated Item",
            "description": "Updated description"
        })

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Updated Item",
        "description": "Updated description"
    }

@pytest.mark.asyncio
async def test_update_item_failure(monkeypatch):
    # Mock the get_item_by_id function to simulate item not found
    async def mock_get_item_by_id(item_id: int):
        return None

    monkeypatch.setattr("app.main.get_item_by_id", mock_get_item_by_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={
            "name": "Updated Item",
            "description": "Updated description"
        })

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

@pytest.mark.asyncio
async def test_delete_item_success(monkeypatch):
    # Mock the get_item_by_id and delete_item functions
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Test Item", "description": "Test description"}

    async def mock_delete_item(item_id: int):
        return True  # Simulate successful deletion

    monkeypatch.setattr("app.main.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.main.delete_item", mock_delete_item)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete("/items/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}

@pytest.mark.asyncio
async def test_delete_item_failure(monkeypatch):
    # Mock the get_item_by_id function to simulate item not found
    async def mock_get_item_by_id(item_id: int):
        return None

    monkeypatch.setattr("app.main.get_item_by_id", mock_get_item_by_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete("/items/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
