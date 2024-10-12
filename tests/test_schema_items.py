import pytest
from pydantic import ValidationError
from app.schemas.item import ItemCreate, ItemUpdate
from app.utils.constants import MAX_DESCRIPTION_LENGTH, MAX_NAME_LENGTH, MIN_DESCRIPTION_LENGTH, MIN_NAME_LENGTH

def test_item_create_valid_data():
    """
    Testcase: Create Item with Valid Data
    - To verify that an item is successfully created when valid name and description are provided.

    Steps:
    1. Define valid data for both name and description.
    2. Create an instance of ItemCreate with the valid data.
    3. Assert that the name and description are correctly set without any errors.

    Result(s):
    - The item is created successfully with the correct name and description.
    """
    # Step 1: Define valid data for both name and description
    valid_data = {
        "name": "Valid Item Name",
        "description": "Valid Item Description"
    }
    # Step 2: Create an instance of ItemCreate with the valid data
    item = ItemCreate(**valid_data)
    # Step 3: Assert that the name and description match the input data
    assert item.name == valid_data["name"]
    assert item.description == valid_data["description"]

def test_item_create_name_too_short():
    """
    Testcase: Create Item with Name Too Short
    - To verify that a ValidationError is raised when the name is shorter than the allowed minimum length.

    Steps:
    1. Define invalid data where the name is an empty string (shorter than the minimum length).
    2. Attempt to create an instance of ItemCreate with the invalid data.
    3. Capture the ValidationError and assert that the error message matches the expected message.

    Result(s):
    - A ValidationError is raised indicating that the name must meet the minimum length requirement.
    """
    # Step 1: Define invalid data where the name is too short (empty string)
    invalid_data = {
        "name": "",  # Invalid empty string
        "description": "Created Item Description"
    }
    
    # Step 2: Attempt to create an instance of ItemCreate with the invalid data
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(**invalid_data)
    
    # Step 3: Assert that the ValidationError is raised and check for the appropriate error message
    assert f"Name must be at least {MIN_NAME_LENGTH} character(s)" in str(exc_info.value)

def test_item_create_name_too_long():
    """
    Testcase: Create Item with Name Too Long
    - To verify that a ValidationError is raised when the name exceeds the maximum allowed length.

    Steps:
    1. Define invalid data where the name is longer than the maximum allowed length.
    2. Attempt to create an instance of ItemCreate with the invalid data.
    3. Capture the ValidationError and assert that the error message matches the expected message.

    Result(s):
    - A ValidationError is raised indicating that the name must not exceed the maximum length.
    """
    # Step 1: Define invalid data where the name exceeds the maximum length allowed
    invalid_data = {
        "name": "a" * (MAX_NAME_LENGTH + 1),  # One character longer than the maximum length
        "description": "Valid Item Description"
    }
    
    # Step 2: Attempt to create an instance of ItemCreate with the invalid data
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(**invalid_data)
    
    # Step 3: Assert that the ValidationError is raised and check for the appropriate error message
    assert f"Name must not exceed {MAX_NAME_LENGTH} character(s)" in str(exc_info.value)

def test_item_create_description_too_short():
    """
    Testcase: Create Item with Description Too Short
    - To verify that a ValidationError is raised when the description is shorter than the allowed minimum length.

    Steps:
    1. Define invalid data where the description is shorter than the minimum length (empty string).
    2. Attempt to create an instance of ItemCreate with the invalid data.
    3. Capture the ValidationError and assert that the error message matches the expected message.

    Result(s):
    - A ValidationError is raised indicating that the description must meet the minimum length.
    """
    # Step 1: Define invalid data where the description is too short (empty string)
    invalid_data = {
        "name": "Valid Item Name",
        "description": ""  # Invalid empty string
    }
    
    # Step 2: Attempt to create an instance of ItemCreate with the invalid data
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(**invalid_data)
    
    # Step 3: Assert that the ValidationError is raised and check for the appropriate error message
    assert f"Description must be at least {MIN_DESCRIPTION_LENGTH} character(s)" in str(exc_info.value)

def test_item_create_description_too_long():
    """
    Testcase: Create Item with Description Too Long
    - To verify that a ValidationError is raised when the description exceeds the maximum allowed length.

    Steps:
    1. Define invalid data where the description is longer than the maximum allowed length.
    2. Attempt to create an instance of ItemCreate with the invalid data.
    3. Capture the ValidationError and assert that the error message matches the expected message.

    Result(s):
    - A ValidationError is raised indicating that the description must not exceed the maximum length.
    """
    # Step 1: Define invalid data where the description exceeds the maximum length allowed
    invalid_data = {
        "name": "Valid Item Name",
        "description": "a" * (MAX_DESCRIPTION_LENGTH + 1)  # One character longer than the maximum length
    }
    
    # Step 2: Attempt to create an instance of ItemCreate with the invalid data
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(**invalid_data)
    
    # Step 3: Assert that the ValidationError is raised and check for the appropriate error message
    assert f"Description must not exceed {MAX_DESCRIPTION_LENGTH} character(s)" in str(exc_info.value)

def test_item_update_name_too_short():
    """
    Testcase: Update Item with Name Too Short
    - To verify that a ValidationError is raised when the name is shorter than the allowed minimum length.

    Steps:
    1. Define invalid data where the name is an empty string (shorter than the minimum length).
    2. Attempt to create an instance of ItemUpdate with the invalid data.
    3. Capture the ValidationError and assert that the error message matches the expected message.

    Result(s):
    - A ValidationError is raised indicating that the name must meet the minimum length.
    """
    # Step 1: Define invalid data where the name is too short (empty string)
    invalid_data = {
        "name": "",  # Invalid empty string
        "description": "Updated Item Description"
    }
    
    # Step 2: Attempt to create an instance of ItemUpdate with the invalid data
    with pytest.raises(ValidationError) as exc_info:
        ItemUpdate(**invalid_data)
    
    # Step 3: Assert that the ValidationError is raised and check for the appropriate error message
    assert f"Name must be at least {MIN_NAME_LENGTH} character(s)" in str(exc_info.value)

def test_item_update_description_too_long():
    """
    Testcase: Update Item with Description Too Long
    - To verify that a ValidationError is raised when the description exceeds the maximum allowed length.

    Steps:
    1. Define invalid data where the description is longer than the maximum allowed length.
    2. Attempt to create an instance of ItemUpdate with the invalid data.
    3. Capture the ValidationError and assert that the error message matches the expected message.

    Result(s):
    - A ValidationError is raised indicating that the description must not exceed the maximum length.
    """
    # Step 1: Define invalid data where the description exceeds the maximum length allowed
    invalid_data = {
        "name": "Updated Item Name",
        "description": "a" * (MAX_DESCRIPTION_LENGTH + 1)  # One character longer than the maximum length
    }
    
    # Step 2: Attempt to create an instance of ItemUpdate with the invalid data
    with pytest.raises(ValidationError) as exc_info:
        ItemUpdate(**invalid_data)
    
    # Step 3: Assert that the ValidationError is raised and check for the appropriate error message
    assert f"Description must not exceed {MAX_DESCRIPTION_LENGTH} character(s)" in str(exc_info.value)
