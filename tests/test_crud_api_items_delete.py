import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Import the FastAPI app
from app.api.endpoints.items import create_item, get_item_by_id  # Import the CRUD operations from the correct module

@pytest.mark.asyncio
async def test_delete_item_success(monkeypatch):
    """
    Testcase: Successful deletion of an item.
    
    Steps:
    1. Monkeypatch `get_item_by_id` to simulate finding the item to be deleted.
    2. Monkeypatch `delete_item` to simulate successful item deletion.
    3. Use `AsyncClient` to send a DELETE request to delete the item.
    4. Verify the response status code and the success message.
    
    Expectation:
    - The API should return a 200 status code indicating successful deletion.
    - The returned JSON message should confirm the item was deleted.
    
    Result(s):
    - Test passes if the item is successfully deleted and the correct success message is returned.
    """
    # Step 1: Mock the get_item_by_id function to simulate finding an item
    async def mock_get_item_by_id(item_id: int):
        return {"id": item_id, "name": "Test Item", "description": "Test description"}

    # Step 2: Mock the delete_item function to simulate successful deletion
    async def mock_delete_item(item_id: int):
        return True  # Simulate successful deletion

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)
    monkeypatch.setattr("app.api.endpoints.items.delete_item", mock_delete_item)

    # Step 3: Send a DELETE request using AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete("/items/1")

    # Step 4: Verify the response status and message
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}

@pytest.mark.asyncio
async def test_delete_item_failure(monkeypatch):
    """
    Testcase: Failure in deleting an item (item not found).
    
    Steps:
    1. Monkeypatch `get_item_by_id` to simulate a case where the item is not found.
    2. Use `AsyncClient` to send a DELETE request to delete a non-existent item.
    3. Verify the response status code is 404 and the appropriate error message is returned.
    
    Expectation:
    - The API should return a 404 status code indicating that the item was not found.
    - The returned JSON message should indicate the item was not found.
    
    Result(s):
    - Test passes if the correct 404 error is returned with the expected error message.
    """
    # Step 1: Mock the get_item_by_id function to simulate an item not found
    async def mock_get_item_by_id(item_id: int):
        return None  # Simulate item not found

    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    # Step 2: Send a DELETE request using AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete("/items/1")

    # Step 3: Verify the response status and error message
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
