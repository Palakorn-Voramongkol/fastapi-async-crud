import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Import the FastAPI app
from fastapi.testclient import TestClient
from fastapi import status

@pytest.mark.asyncio
async def test_delete_item_success(monkeypatch):
    """
    Test Case: Successful deletion of an item.

    This test mocks both the `get_item_by_id` and `delete_item` functions to simulate
    the successful deletion of an item.

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
    Test Case: Failure in deleting an item (item not found).

    This test mocks the `get_item_by_id` function to simulate a case where the item is not found,
    and then verifies the API correctly returns a 404 status code.

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

client = TestClient(app)
@pytest.mark.asyncio
async def test_delete_item_endpoint_failure(monkeypatch):
    # Define the item ID to be deleted
    item_id = 1

    # Mock get_item_by_id to return a valid item (to pass the 404 check)
    async def mock_get_item_by_id(id: int):
        return {"id": id, "name": "Test Item", "description": "Test Description"}

    # Mock the actual imported function in the endpoint
    monkeypatch.setattr("app.api.endpoints.items.get_item_by_id", mock_get_item_by_id)

    # Mock delete_item to raise an Exception (simulate failure)
    async def mock_delete_item(id: int):
        raise Exception("Database error")

    monkeypatch.setattr("app.api.endpoints.items.delete_item", mock_delete_item)

    # Debug prints to ensure the mocks are working
    print("Mocks applied. Simulating delete_item failure...")

    # Make the delete request and verify the response
    response = client.delete(f"/items/{item_id}")

    # Debug print the response details
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")

    # Assertions to check for HTTP 500 response and error message
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Failed to delete item: Database error"}
