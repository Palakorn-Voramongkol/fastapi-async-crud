import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Import the FastAPI app
from app.api.endpoints.items import create_item, get_item_by_id  # Import the CRUD operations from the correct module

@pytest.mark.asyncio
async def test_create_item_success(monkeypatch):
    """
    Test Case: Simulate successful creation of an item.
    
    This test checks if an item can be successfully created by mocking the `create_item`
    function to return a predefined item. It then sends a POST request to create the item 
    and verifies the response content and status code.
    
    Steps:
    1. Monkeypatch the `create_item` function to simulate item creation.
    2. Use `AsyncClient` to send a POST request to create the item.
    3. Verify the status code and returned JSON data.
    """
    # Mock the create_item function to simulate a successful creation
    async def mock_create_item(name: str, description: str):
        return {"id": 1, "name": name, "description": description}

    # Monkeypatch the function as it's imported in app.api.endpoints.items
    monkeypatch.setattr("app.api.endpoints.items.create_item", mock_create_item)

    # Use ASGITransport with AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items/", json={"name": "Test Item", "description": "This is a test item"})

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item"
    
@pytest.mark.asyncio
async def test_create_item_failure(monkeypatch):
    """
    Test Case: Simulate failure during item creation.
    
    This test simulates an exception being raised during item creation by mocking the
    `create_item` function to raise an exception. It sends a POST request to create the
    item and checks that the error is handled with the appropriate status code and message.
    
    Steps:
    1. Monkeypatch `create_item` to simulate a failure.
    2. Send a POST request to create the item.
    3. Verify the status code is 400, and the error message is correctly returned.
    """
    # Mock the create_item function to simulate an exception
    async def mock_create_item(name: str, description: str):
        raise Exception("Simulated exception")

    monkeypatch.setattr("app.api.endpoints.items.create_item", mock_create_item)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items/", json={"name": "Test Item", "description": "This is a test item"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to create item: Simulated exception"}


@pytest.mark.asyncio
async def test_read_item_success(monkeypatch):
    """
    Test Case: Simulate successful reading of an item.
    
    This test mocks the `get_item_by_id` function to simulate a successful item retrieval.
    It sends a GET request to retrieve an item and checks the returned data and status code.
    
    Steps:
    1. Monkeypatch the `get_item_by_id` function to simulate an existing item.
    2. Use `AsyncClient` to send a GET request to retrieve the item.
    3. Verify the status code and returned JSON data.
    """
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Test Item", "description": "This is a test item"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

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
    """
    Test Case: Simulate failure in reading an item (item not found).
    
    This test mocks the `get_item_by_id` function to simulate a case where the item does
    not exist. It sends a GET request to retrieve a non-existent item and verifies the 
    correct 404 status code and error message.
    
    Steps:
    1. Monkeypatch `get_item_by_id` to return None (item not found).
    2. Send a GET request to retrieve the non-existent item.
    3. Verify the status code is 404 and the error message is returned.
    """
    async def mock_get_item_by_id(item_id: int):
        return None  # Simulate item not found

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/items/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

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
    """
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    async def mock_update_item(item_id: int, name: str, description: str):
        return {"id": item_id, "name": name, "description": description}

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
    """
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    async def mock_update_item(item_id: int, name: str = None, description: str = None):
        return {"id": item_id, "name": name, "description": "Old description"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.api.endpoints.items.update_item", mock_update_item)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "Updated Item"})

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
    """
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    async def mock_update_item(item_id: int, name: str = None, description: str = None):
        return {"id": item_id, "name": "Old Item", "description": description}

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
async def test_delete_item_success(monkeypatch):
    """
    Test Case: Simulate successful deletion of an item.
    
    This test mocks both the `get_item_by_id` and `delete_item` functions to simulate 
    the successful deletion of an item. It sends a DELETE request to remove the item and 
    verifies the status code and success message.
    
    Steps:
    1. Monkeypatch `get_item_by_id` to simulate finding the item.
    2. Monkeypatch `delete_item` to simulate item deletion.
    3. Send a DELETE request to delete the item.
    4. Verify the status code and success message.
    """
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Test Item", "description": "Test description"}

    async def mock_delete_item(item_id: int):
        return True  # Simulate successful deletion

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.api.endpoints.items.delete_item", mock_delete_item)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete("/items/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}

@pytest.mark.asyncio
async def test_delete_item_failure(monkeypatch):
    """
    Test Case: Simulate failure in deleting an item (item not found).
    
    This test mocks the `get_item_by_id` function to simulate a case where the item does
    not exist. It sends a DELETE request to delete the non-existent item and verifies the 
    correct 404 status code and error message.
    
    Steps:
    1. Monkeypatch `get_item_by_id` to return None (item not found).
    2. Send a DELETE request to delete the non-existent item.
    3. Verify the status code is 404 and the error message is returned.
    """
    async def mock_get_item_by_id(item_id: int):
        return None

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete("/items/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


@pytest.mark.asyncio
async def test_create_item_empty_name():
    """
    Test Case: Attempt to create an item with an empty name.

    This test ensures that the API returns a 422 status code when attempting to create
    an item with an empty name.

    Steps:
    1. Send a POST request to create an item with an empty name.
    2. Verify that the API responds with a 422 status code and the appropriate error message.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items/", json={"name": "", "description": "Test Description"})

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "String should have at least 1 character",
                "type": "string_too_short",
                "ctx": {"min_length": 1},
                "input": ""
            }
        ]
    }



@pytest.mark.asyncio
async def test_create_item_empty_description():
    """
    Test Case: Attempt to create an item with an empty description.

    This test ensures that the API returns a 422 status code when attempting to create
    an item with an empty description.

    Steps:
    1. Send a POST request to create an item with an empty description.
    2. Verify that the API responds with a 422 status code and the appropriate error message.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items/", json={"name": "Test Item", "description": ""})

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "description"],
                "msg": "String should have at least 1 character",
                "type": "string_too_short",
                "ctx": {"min_length": 1},
                "input": ""
            }
        ]
    }



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
    """
    # Mock the get_item_by_id to simulate item not found
    async def mock_get_item_by_id(item_id: int):
        return None  # Simulate item not found

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "New Name", "description": "New Description"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


@pytest.mark.asyncio
async def test_update_item_empty_name(monkeypatch):
    """
    Test Case: Attempt to update an item with an empty name.
    
    This test mocks the `get_item_by_id` function to simulate an existing item, 
    and then sends a PUT request to update the item with an empty name. The API should return a 422 status code.
    
    Steps:
    1. Monkeypatch `get_item_by_id` to simulate an existing item.
    2. Send a PUT request to update the item with an empty name.
    3. Verify that the API responds with a 422 status code and the appropriate error message.
    """
    # Mock the get_item_by_id to simulate item found
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "", "description": "Updated description"})

    assert response.status_code == 422
    assert response.json() == {"detail": "Name cannot be empty"}


@pytest.mark.asyncio
async def test_update_item_empty_description(monkeypatch):
    """
    Test Case: Attempt to update an item with an empty description.
    
    This test mocks the `get_item_by_id` function to simulate an existing item, 
    and then sends a PUT request to update the item with an empty description. The API should return a 422 status code.
    
    Steps:
    1. Monkeypatch `get_item_by_id` to simulate an existing item.
    2. Send a PUT request to update the item with an empty description.
    3. Verify that the API responds with a 422 status code and the appropriate error message.
    """
    # Mock the get_item_by_id to simulate item found
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "Updated Item", "description": ""})

    assert response.status_code == 422
    assert response.json() == {"detail": "Description cannot be empty"}


@pytest.mark.asyncio
async def test_update_item_failure(monkeypatch):
    """
    Test Case: Simulate failure during item update.
    
    This test mocks both the `get_item_by_id` and `update_item` functions to simulate a failure during the update operation.
    The API should return a 500 status code when the update fails unexpectedly.
    
    Steps:
    1. Monkeypatch `get_item_by_id` to simulate an existing item.
    2. Monkeypatch `update_item` to simulate an update failure.
    3. Send a PUT request to update the item.
    4. Verify that the API responds with a 500 status code and the appropriate error message.
    """
    # Mock the get_item_by_id to simulate item found
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    # Mock the update_item to simulate update failure
    async def mock_update_item(item_id: int, name: str, description: str):
        return None  # Simulate update failure

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.api.endpoints.items.update_item", mock_update_item)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "Updated Item", "description": "Updated description"})

    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to update item"}
