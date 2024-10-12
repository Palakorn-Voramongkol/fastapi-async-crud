import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Import the FastAPI app
from app.api.endpoints.items import create_item, get_item_by_id  # Import the CRUD operations from the correct module

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
    # Step 1: Monkeypatch to simulate finding an existing item
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    # Step 2: Monkeypatch to simulate successful item update
    async def mock_update_item(item_id: int, name: str, description: str):
        return {"id": item_id, "name": name, "description": description}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.api.endpoints.items.update_item", mock_update_item)

    # Step 3: Send PUT request to update the item
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={
            "name": "Updated Item",
            "description": "Updated description"
        })

    # Step 4: Verify the status code and updated item data
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Updated Item",
        "description": "Updated description"
    }

@pytest.mark.asyncio
async def test_update_item_success_with_optional_fields(monkeypatch):
    """
    Test Case: Simulate successful update of an item with only optional fields.

    This test mocks both the `get_item_by_id` and `update_item` functions to simulate
    a successful update operation where only optional fields (name or description) are updated.

    Steps:
    1. Monkeypatch `get_item_by_id` to simulate finding the item.
    2. Monkeypatch `update_item` to simulate updating only optional fields.
    3. Send a PUT request to update the item.
    4. Verify the status code and returned updated item data.

    Expectation:
    - The item should be successfully updated with optional fields, and the response should return the updated item data.

    Result(s):
    - Test passes if the status code is 200, and the returned data matches the updated input.
    """
    # Step 1: Monkeypatch to simulate finding an existing item
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    # Step 2: Monkeypatch to simulate updating the item with optional fields
    async def mock_update_item(item_id: int, name: str = None, description: str = None):
        return {"id": item_id, "name": name or "Old Item", "description": description or "Old description"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.api.endpoints.items.update_item", mock_update_item)

    # Step 3: Send PUT request to update the item
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "Updated Item", "description": "Updated description"})

    # Step 4: Verify the status code and updated item data
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

    Steps:
    1. Monkeypatch `get_item_by_id` to return None (item not found).
    2. Send a PUT request to update the non-existent item.
    3. Verify the status code is 404 and the error message is returned.

    Expectation:
    - If the item does not exist, the response should return a 404 status code and an appropriate error message.

    Result(s):
    - Test passes if the status code is 404, and the error message indicates that the item was not found.
    """
    # Step 1: Monkeypatch to simulate item not found
    async def mock_get_item_by_id(item_id: int):
        return None

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    # Step 2: Send PUT request for a non-existent item
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={
            "name": "Updated Item",
            "description": "Updated description"
        })

    # Step 3: Verify 404 status code and error message
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

@pytest.mark.asyncio
async def test_update_item_not_found(monkeypatch):
    """
    Test Case: Attempt to update an item that doesn't exist.

    This test mocks the `get_item_by_id` function to simulate a non-existent item, 
    then sends a PUT request to update the item. The API should return a 404 status code.

    Steps:
    1. Monkeypatch `get_item_by_id` to simulate an item not found.
    2. Send a PUT request to update the item.
    3. Verify that the API responds with a 404 status code and the appropriate error message.

    Expectation:
    - If the item does not exist, the response should return a 404 status code and an appropriate error message.

    Result(s):
    - Test passes if the status code is 404, and the error message indicates that the item was not found.
    """
    # Step 1: Monkeypatch to simulate item not found
    async def mock_get_item_by_id(item_id: int):
        return None  # Simulate item not found

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    # Step 2: Send PUT request for a non-existent item
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "New Name", "description": "New Description"})

    # Step 3: Verify 404 status code and error message
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

@pytest.mark.asyncio
async def test_update_item_name_only(monkeypatch):
    """
    Test Case: Simulate updating only the name of an item.

    This test mocks both the `get_item_by_id` and `update_item` functions to simulate
    a successful update operation where only the name is updated, while the description remains unchanged.

    Steps:
    1. Monkeypatch `get_item_by_id` to simulate finding the item.
    2. Monkeypatch `update_item` to simulate updating the item's name only.
    3. Send a PUT request to update the item.
    4. Verify the status code and returned updated item data.

    Expectation:
    - The item's name should be updated successfully, and the description should remain unchanged.

    Result(s):
    - Test passes if the name is updated, the description remains unchanged, and the status code is 200.
    """
    # Step 1: Monkeypatch to simulate finding an existing item
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    # Step 2: Monkeypatch to simulate updating only the name
    async def mock_update_item(item_id: int, name: str = None, description: str = None):
        return {"id": item_id, "name": name, "description": "Old description"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.api.endpoints.items.update_item", mock_update_item)

    # Step 3: Send PUT request to update only the name
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "Updated Item"})

    # Step 4: Verify the status code and updated name
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Updated Item",
        "description": "Old description"
    }

@pytest.mark.asyncio
async def test_update_item_description_only(monkeypatch):
    """
    Test Case: Simulate updating only the description of an item.

    This test mocks both the `get_item_by_id` and `update_item` functions to simulate
    a successful update operation where only the description is updated, while the name remains unchanged.

    Steps:
    1. Monkeypatch `get_item_by_id` to simulate finding the item.
    2. Monkeypatch `update_item` to simulate updating the item's description only.
    3. Send a PUT request to update the item.
    4. Verify the status code and returned updated item data.

    Expectation:
    - The item's description should be updated successfully, while the name remains unchanged.

    Result(s):
    - Test passes if the description is updated, the name remains unchanged, and the status code is 200.
    """
    # Step 1: Monkeypatch to simulate finding an existing item
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    # Step 2: Monkeypatch to simulate updating only the description
    async def mock_update_item(item_id: int, name: str = None, description: str = None):
        return {"id": item_id, "name": "Old Item", "description": description}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.api.endpoints.items.update_item", mock_update_item)

    # Step 3: Send PUT request to update only the description
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"description": "Updated description"})

    # Step 4: Verify the status code and updated description
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Old Item",
        "description": "Updated description"
    }

@pytest.mark.asyncio
async def test_update_item_name_too_long(monkeypatch):
    """
    Test Case: Attempt to update an item with a name that exceeds the maximum length.

    This test ensures that the API returns a 422 status code when attempting to update
    an item with a name longer than 100 characters.

    Steps:
    1. Monkeypatch `get_item_by_id` to simulate finding the item.
    2. Send a PUT request with a name longer than 100 characters.
    3. Verify the status code is 422 and the error message is returned.

    Expectation:
    - The API should return a 422 status code and an appropriate validation error for a name that is too long.

    Result(s):
    - Test passes if the status code is 422 and the error message indicates the name is too long.
    """
    # Step 1: Monkeypatch to simulate finding an existing item
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    # Step 2: Send PUT request with a long name
    long_name = "a" * 101  # Name longer than the max length of 100 characters
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": long_name, "description": "Updated description"})

    # Step 3: Verify 422 status code and validation error message
    assert response.status_code == 422
    response_data = response.json()
    assert "Value error" in response_data["detail"][0]["msg"]

@pytest.mark.asyncio
async def test_update_item_name_too_short(monkeypatch):
    """
    Test Case: Attempt to update an item with a name that is shorter than the minimum length.

    This test ensures that the API returns a 422 status code when attempting to update
    an item with a name shorter than 1 character.

    Steps:
    1. Monkeypatch `get_item_by_id` to simulate finding the item.
    2. Send a PUT request with a name shorter than 1 character.
    3. Verify the status code is 422 and the error message is returned.

    Expectation:
    - The API should return a 422 status code and an appropriate validation error for a name that is too short.

    Result(s):
    - Test passes if the status code is 422 and the error message indicates the name is too short.
    """
    # Step 1: Monkeypatch to simulate finding an existing item
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    # Step 2: Send PUT request with a too-short name
    short_name = ""  # Name shorter than the min length of 1 character
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": short_name, "description": "Updated description"})

    # Step 3: Verify 422 status code and validation error message
    assert response.status_code == 422
    response_data = response.json()
    assert "Value error" in response_data["detail"][0]["msg"]
