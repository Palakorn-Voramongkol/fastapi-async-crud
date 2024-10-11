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
async def test_get_items_with_pagination():
    """
    Test Case: Retrieve items with pagination.

    This test verifies that the API supports pagination by retrieving items
    in paginated chunks and ensuring the correct number of items is returned.

    Steps:
    1. Create multiple items (for testing pagination).
    2. Send a GET request to retrieve a limited number of items.
    3. Verify the number of returned items matches the limit.
    """
    # Step 1: Create 100 items for testing
    async def create_test_items(num_items=100):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            for i in range(num_items):
                item_data = {"name": f"Item {i}", "description": f"Description {i}"}
                await ac.post("/items/", json=item_data)

    await create_test_items()

    # Step 2: Retrieve items with pagination (limit=10, offset=0)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/items/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        data = response.json()

        # Step 3: Verify 10 items were returned
        assert len(data) == 10

        # Step 4: Test the next page with offset
        response = await ac.get("/items/", params={"limit": 10, "offset": 10})
        assert response.status_code == 200
        data = response.json()

        # Verify 10 more items were returned (i.e., the next 10 items)
        assert len(data) == 10



@pytest.mark.asyncio
async def test_create_item_name_too_long():
    """
    Test Case: Attempt to create an item with a name that exceeds the maximum length.

    This test ensures that the API returns a 422 status code when attempting to create
    an item with a name longer than 100 characters.
    """
    # Generate a string that exceeds the max length of 100 characters for name
    long_name = "a" * 101
    item_data = {"name": long_name, "description": "Valid description"}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items/", json=item_data)

    # Assert that the API returns a 422 status code for validation error
    assert response.status_code == 422
    response_data = response.json()

    # Adjust the assertion to match the actual error response format
    assert response_data["detail"][0]["loc"] == ["body", "name"]
    assert "max_length" in response_data["detail"][0]["ctx"]
    assert response_data["detail"][0]["ctx"]["max_length"] == 100

@pytest.mark.asyncio
async def test_create_item_description_too_long():
    """
    Test Case: Attempt to create an item with a description that exceeds the maximum length.

    This test ensures that the API returns a 422 status code when attempting to create
    an item with a description longer than 500 characters.
    """
    # Generate a string that exceeds the max length of 500 characters for description
    long_description = "a" * 501
    item_data = {"name": "Valid name", "description": long_description}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items/", json=item_data)

    # Assert that the API returns a 422 status code for validation error
    assert response.status_code == 422
    response_data = response.json()

    # Adjust the assertion to match the actual error response format
    assert response_data["detail"][0]["loc"] == ["body", "description"]
    assert "max_length" in response_data["detail"][0]["ctx"]
    assert response_data["detail"][0]["ctx"]["max_length"] == 500



@pytest.mark.asyncio
async def test_update_item_success(monkeypatch):
    """
    Test Case: Simulate successful update of an item.
    
    This test mocks both the `get_item_by_id` and `update_item` functions to simulate 
    a successful update operation. It sends a PUT request to update the item and verifies 
    the returned updated data.
    """
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    async def mock_update_item(item_id: int, name: str = None, description: str = None):
        return {"id": item_id, "name": name or "Old Item", "description": description or "Old description"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.api.endpoints.items.update_item", mock_update_item)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": "Updated Item", "description": "Updated description"})

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Updated Item",
        "description": "Updated description"
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
async def test_update_item_name_too_long(monkeypatch):
    """
    Test Case: Attempt to update an item with a name that exceeds the maximum length.
    
    This test ensures that the API returns a 422 status code when attempting to update
    an item with a name longer than 100 characters.
    """
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    long_name = "a" * 101  # Name longer than the max length of 100 characters

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": long_name, "description": "Updated description"})

    assert response.status_code == 422
    response_data = response.json()
    assert response_data["detail"][0]["loc"] == ["body", "name"]
    assert response_data["detail"][0]["msg"] == "String should have at most 100 characters"  # Updated expected message

@pytest.mark.asyncio
async def test_update_item_name_too_short(monkeypatch):
    """
    Test Case: Attempt to update an item with a name that is shorter than the minimum length.
    
    This test ensures that the API returns a 422 status code when attempting to update
    an item with a name shorter than 1 character.
    """
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Old Item", "description": "Old description"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    short_name = ""  # Name shorter than the min length of 1 character

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.put("/items/1", json={"name": short_name, "description": "Updated description"})

    assert response.status_code == 422
    response_data = response.json()
    assert response_data["detail"][0]["loc"] == ["body", "name"]
    assert response_data["detail"][0]["msg"] == "String should have at least 1 character"  # Updated expected message
