import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Import the FastAPI app
from app.schemas.item import ItemUpdate  # Import the Pydantic schema for updating items


@pytest.mark.asyncio
async def test_update_item_success(monkeypatch):
    """
    Test Case: Simulate successful update of an item.

    This test mocks both the `get_item_by_id` and `update_item` functions to simulate
    a successful update operation. It sends a PUT request to update the item and verifies
    the returned updated data.

    Steps:
    1. Monkeypatch `get_item_by_id` to simulate finding the item.
    2. Monkeypatch `update_item` to simulate updating the item.
    3. Send a PUT request to update the item.
    4. Verify the status code and returned updated item data.

    Expectation:
    - The item should be successfully updated, and the response should return the updated item data.

    Result(s):
    - Test passes if the status code is 200, and the returned data matches the updated input.
    """
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    async def mock_update_item(item_id: int, item_data: ItemUpdate):
        return {"id": item_id, "name": item_data.name, "description": item_data.description}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.api.endpoints.items.update_item", mock_update_item)

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
    """
    Test Case: Simulate failure in updating an item (item not found).

    This test mocks the `get_item_by_id` function to simulate a case where the item does
    not exist. It sends a PUT request to update the non-existent item and verifies the
    correct 404 status code and error message.
    """
    async def mock_get_item_by_id(item_id: int):
        return None

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={
            "name": "Updated Item",
            "description": "Updated description"
        })

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


@pytest.mark.asyncio
async def test_update_item_name_too_long(monkeypatch):
    """
    Test Case: Attempt to update an item with a name that exceeds the maximum length.

    This test ensures that the API returns a 422 status code when attempting to update
    an item with a name longer than 100 characters.
    """
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    long_name = "a" * 101
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": long_name, "description": "Updated description"})

    assert response.status_code == 422
    response_data = response.json()
    assert "value_error" in response_data["detail"][0]["type"]


@pytest.mark.asyncio
async def test_update_item_description_only(monkeypatch):
    """
    Test Case: Simulate updating only the description of an item.

    This test mocks both the `get_item_by_id` and `update_item` functions to simulate
    a successful update operation where only the description is updated.
    """
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    async def mock_update_item(item_id: int, item_data: ItemUpdate):
        return {"id": item_id, "name": "Old Item", "description": item_data.description}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.api.endpoints.items.update_item", mock_update_item)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"description": "Updated description"})

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Old Item",
        "description": "Updated description"
    }
