import pytest
from pydantic import ValidationError
from app.schemas.item import ItemCreate, ItemUpdate
from app.utils.constants import MAX_DESCRIPTION_LENGTH, MAX_NAME_LENGTH, MIN_DESCRIPTION_LENGTH, MIN_NAME_LENGTH

def test_item_create_valid_data():
    """
    Test case for creating an item with valid name and description.
    This should pass without raising any ValidationError.
    """
    valid_data = {
        "name": "Valid Item Name",
        "description": "Valid Item Description"
    }
    item = ItemCreate(**valid_data)
    assert item.name == valid_data["name"]
    assert item.description == valid_data["description"]

def test_item_create_name_too_short():
    """
    Test case for creating an item with a name that's too short.
    This should raise a ValidationError because the name is an empty string.
    """
    invalid_data = {
        "name": "",  # Invalid empty string, which is shorter than the minimum length
        "description": "Created Item Description"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(**invalid_data)
    
    assert f"Name must be at least {MIN_NAME_LENGTH} characters long." in str(exc_info.value)

def test_item_create_name_too_long():
    """
    Test case for creating an item with a name that's too long.
    This should raise a ValidationError because the name exceeds the maximum allowed length.
    """
    invalid_data = {
        "name": "a" * (MAX_NAME_LENGTH + 1),  # One character longer than the maximum length
        "description": "Valid Item Description"
    }
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(**invalid_data)
    
    assert f"Name must not exceed {MAX_NAME_LENGTH} characters." in str(exc_info.value)

def test_item_create_description_too_short():
    """
    Test case for creating an item with a description that's too short.
    This should raise a ValidationError because the description is an empty string.
    """
    invalid_data = {
        "name": "Valid Item Name",
        "description": ""  # Invalid empty string, which is shorter than the minimum length
    }
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(**invalid_data)
    
    assert f"Description must be at least {MIN_DESCRIPTION_LENGTH} characters long." in str(exc_info.value)

def test_item_create_description_too_long():
    """
    Test case for creating an item with a description that's too long.
    This should raise a ValidationError because the description exceeds the maximum allowed length.
    """
    invalid_data = {
        "name": "Valid Item Name",
        "description": "a" * (MAX_DESCRIPTION_LENGTH + 1)  # One character longer than the maximum length
    }
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(**invalid_data)
    
    assert f"Description must not exceed {MAX_DESCRIPTION_LENGTH} characters." in str(exc_info.value)

def test_item_update_name_too_short():
    """
    Test case for updating an item with a name that's too short.
    This should raise a ValidationError because the name is an empty string.
    """
    invalid_data = {
        "name": "",  # Invalid empty string
        "description": "Updated Item Description"
    }
    with pytest.raises(ValidationError) as exc_info:
        ItemUpdate(**invalid_data)
    
    assert f"Name must be at least {MIN_NAME_LENGTH} characters long." in str(exc_info.value)

def test_item_update_description_too_long():
    """
    Test case for updating an item with a description that's too long.
    This should raise a ValidationError because the description exceeds the maximum allowed length.
    """
    invalid_data = {
        "name": "Updated Item Name",
        "description": "a" * (MAX_DESCRIPTION_LENGTH + 1)  # One character longer than the maximum length
    }
    with pytest.raises(ValidationError) as exc_info:
        ItemUpdate(**invalid_data)
    
    assert f"Description must not exceed {MAX_DESCRIPTION_LENGTH} characters." in str(exc_info.value)
