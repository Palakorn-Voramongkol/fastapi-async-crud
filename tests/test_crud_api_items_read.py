import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Import the FastAPI app
from app.schemas.item import ItemCreate  # Import the Pydantic schema for item creation


@pytest.mark.asyncio
async def test_read_item_success(monkeypatch):
    """
    Testcase: Successful retrieval of an item.
    
    Steps:
    1. Monkeypatch the `get_item_by_id` function to simulate an existing item.
    2. Use `AsyncClient` to send a GET request to retrieve the item by its ID.
    3. Verify the status code is 200 and check the returned JSON data for correctness.
    
    Expectation:
    - The API should return a 200 status code for successful retrieval.
    - The returned JSON data should match the mocked item's details.
    
    Result(s):
    - Test passes if the API successfully returns the item with the correct details.
    """
    # Step 1: Mock the get_item_by_id function to simulate finding an item
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Test Item", "description": "This is a test item"}

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    # Step 2: Send a GET request using AsyncClient to retrieve the item
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/items/1")

    # Step 3: Verify the status code and returned data
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Test Item",
        "description": "This is a test item"
    }


@pytest.mark.asyncio
async def test_read_item_failure(monkeypatch):
    """
    Testcase: Failed retrieval of an item (item not found).
    
    Steps:
    1. Monkeypatch the `get_item_by_id` function to simulate a case where the item is not found.
    2. Use `AsyncClient` to send a GET request to retrieve the non-existent item.
    3. Verify the status code is 404 and check the returned error message.
    
    Expectation:
    - The API should return a 404 status code indicating that the item was not found.
    - The returned JSON data should contain an appropriate error message.
    
    Result(s):
    - Test passes if the correct 404 error is returned with the expected message.
    """
    # Step 1: Mock the get_item_by_id function to simulate the item not found
    async def mock_get_item_by_id(item_id: int):
        return None  # Simulate item not found

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    # Step 2: Send a GET request using AsyncClient to retrieve the non-existent item
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/items/1")

    # Step 3: Verify the status code and error message
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


@pytest.mark.asyncio
async def test_get_items_with_pagination(monkeypatch):
    """
    Testcase: Retrieval of items using pagination.
    
    Steps:
    1. Mock the `get_items` function to return a paginated list of items.
    2. Use `AsyncClient` to send a GET request with pagination parameters (`limit` and `offset`).
    3. Verify that the correct number of items is returned in each paginated request.
    
    Expectation:
    - The API should return the specified number of items per request based on the `limit` parameter.
    - The next paginated request should return the next set of items.
    
    Result(s):
    - Test passes if the correct number of items is returned in each request, and pagination works as expected.
    """
    # Step 1: Mock the `get_items` function to simulate paginated response
    async def mock_get_items(limit: int, offset: int):
        return [{"id": i + offset, "name": f"Item {i + offset}", "description": f"Description {i + offset}"} for i in range(limit)]

    monkeypatch.setattr("app.api.endpoints.items.get_items", mock_get_items)

    # Step 2: Retrieve items with pagination (limit=10, offset=0)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/items/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        data = response.json()

        # Step 3: Verify 10 items were returned
        assert len(data) == 10

        # Step 4: Retrieve the next page of items (limit=10, offset=10)
        response = await ac.get("/items/", params={"limit": 10, "offset": 10})
        assert response.status_code == 200
        data = response.json()

        # Verify that 10 more items were returned in the second request
        assert len(data) == 10
