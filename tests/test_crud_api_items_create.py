import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Import the FastAPI app
from app.schemas.item import ItemCreate  # Import the Pydantic schema for item creation
from app.crud.item import create_item  # Import the create_item method from the correct module


@pytest.mark.asyncio
async def test_create_item_success(monkeypatch):
    """
    Testcase: Successful item creation
    
    Steps:
    1. Monkeypatch the `create_item` function to simulate item creation.
    2. Use `AsyncClient` to send a POST request to create the item with a valid name and description.
    3. Verify the response status code and JSON data for correctness.
    
    Expectation:
    - The status code should be 200.
    - The returned JSON should contain the item ID, name, and description.
    
    Result(s):
    - Test passes if the item is successfully created and the returned data is as expected.
    """
    # Step 1: Mock the create_item function to simulate successful creation
    async def mock_create_item(item_data: ItemCreate):
        return {"id": 1, "name": item_data.name, "description": item_data.description}

    # Monkeypatch the function
    monkeypatch.setattr("app.crud.item.create_item", mock_create_item)

    # Step 2: Use AsyncClient to send the request
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items/", json={"name": "Test Item", "description": "This is a test item"})

    # Step 3: Verify response status and data
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item"




@pytest.mark.asyncio
async def test_create_item_failure(monkeypatch):
    """
    Testcase: Failure during item creation
    
    Steps:
    1. Monkeypatch the `create_item` function to simulate an exception.
    2. Send a POST request to create the item.
    3. Verify the status code is 400 and the error message is returned correctly.
    
    Expectation:
    - The status code should be 400, indicating a failure during creation.
    - The error message should contain the exception details.
    
    Result(s):
    - Test passes if the exception is correctly handled and the appropriate error message is returned.
    """
    # Step 1: Mock the create_item function to simulate an exception
    async def mock_create_item(item_data: ItemCreate):
        raise Exception("Simulated exception")

    # Patch the FastAPI endpoint that uses `create_item`
    monkeypatch.setattr("app.api.endpoints.items.create_item", mock_create_item)

    # Step 2: Send the POST request
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items/", json={"name": "Test Item", "description": "This is a test item"})

    # Step 3: Verify the response status and error message
    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to create item: Simulated exception"}


@pytest.mark.asyncio
async def test_create_item_name_too_long():
    """
    Testcase: Create item with name exceeding maximum length
    
    Steps:
    1. Prepare an item with a name that exceeds 100 characters.
    2. Send a POST request to create the item.
    3. Verify that the response contains a 422 status code and validation error message.
    
    Expectation:
    - The API should return a 422 status code for validation error.
    - The error message should indicate the name exceeds the maximum allowed length.
    
    Result(s):
    - Test passes if the API correctly handles the long name and returns the expected error.
    """
    # Step 1: Generate a long name that exceeds the maximum length
    long_name = "a" * 101
    item_data = {"name": long_name, "description": "Valid description"}

    # Step 2: Send the POST request
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items/", json=item_data)

    # Step 3: Assert validation error response
    assert response.status_code == 422
    response_data = response.json()
    assert "value_error" in response_data["detail"][0]["type"]


@pytest.mark.asyncio
async def test_create_item_description_too_long():
    """
    Testcase: Create item with description exceeding maximum length
    
    Steps:
    1. Prepare an item with a description longer than 500 characters.
    2. Send a POST request to create the item.
    3. Verify that the response contains a 422 status code and validation error message.
    
    Expectation:
    - The API should return a 422 status code for validation error.
    - The error message should indicate the description exceeds the maximum allowed length.
    
    Result(s):
    - Test passes if the API correctly handles the long description and returns the expected error.
    """
    # Step 1: Generate a description longer than the allowed 500 characters
    long_description = "a" * 501
    item_data = {"name": "Valid name", "description": long_description}

    # Step 2: Send the POST request
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/items/", json=item_data)

    # Step 3: Assert validation error response
    assert response.status_code == 422
    response_data = response.json()
    assert "value_error" in response_data["detail"][0]["type"]
