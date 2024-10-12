from pydantic import BaseModel, constr, ConfigDict, Field, ValidationError, field_validator
from typing import Optional
from app.utils.constants import MAX_DESCRIPTION_LENGTH, MAX_NAME_LENGTH, MIN_DESCRIPTION_LENGTH, MIN_NAME_LENGTH

class ItemCreate(BaseModel):
    """
    Pydantic model for creating a new item with custom validation error messages.

    Attributes:
        name (str): The name of the item to be created (non-empty, with a custom error message).
        description (str): A detailed description of the item (non-empty, with a custom error message).
    """
    
    # Use Field to define min and max length for name and description
    name: str 
    description: str

    # Custom field validator for 'name'
    # This method is automatically triggered when the `name` field is set during validation.
    @field_validator("name")
    def validate_name(cls, value):
        # Validate that the name is at least MIN_NAME_LENGTH characters
        if len(value) < MIN_NAME_LENGTH:
            raise ValueError(f"Name must be at least {MIN_NAME_LENGTH} character(s)")
        # Validate that the name does not exceed MAX_NAME_LENGTH characters
        if len(value) > MAX_NAME_LENGTH:
            raise ValueError(f"Name must not exceed {MAX_NAME_LENGTH} character(s)")
        # Return the validated value
        return value
    
    # Custom field validator for 'description'
    @field_validator("description")
    def validate_description(cls, value):
        # Strip leading/trailing spaces and ensure the description meets the minimum length
        if len(value.strip()) < MIN_DESCRIPTION_LENGTH:
            raise ValueError(f"Description must be at least {MIN_DESCRIPTION_LENGTH} character(s)")
        # Ensure the description does not exceed the maximum length
        if len(value) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Description must not exceed {MAX_DESCRIPTION_LENGTH} character(s)")
        # Return the validated value
        return value


class ItemResponse(BaseModel):
    """
    Pydantic model for returning an item in responses.

    Attributes:
        id (int): The unique identifier of the item.
        name (str): The name of the item.
        description (str): A detailed description of the item.
    
    Configuration:
        model_config (ConfigDict): Configuration to enable populating the model directly from database attributes.
    """

    # Fields returned in API responses
    id: int
    name: str
    description: str

    # Enable the population of this model directly from database attributes
    model_config = ConfigDict(from_attributes=True)


class ItemUpdate(BaseModel):
    """
    Pydantic model for updating an existing item.

    Attributes:
        name (Optional[str]): The updated name of the item (optional, can be omitted).
        description (Optional[str]): The updated description of the item (optional, can be omitted).
    """
    
    # Fields that can be updated are optional. If omitted, they will default to None.
    name: Optional[str] = None
    description: Optional[str] = None

    # Custom field validator for 'name'
    # This validator is triggered only when the `name` field is explicitly provided in the input.
    @field_validator("name")
    def validate_name(cls, value):
        # If the field is provided (i.e., not None), perform validation
        if value is not None:
            # Validate that the name meets the minimum length requirement
            if len(value.strip()) < MIN_NAME_LENGTH:
                raise ValueError(f"Name must be at least {MIN_NAME_LENGTH} character(s)")
            # Validate that the name does not exceed the maximum length
            if len(value) > MAX_NAME_LENGTH:
                raise ValueError(f"Name must not exceed {MAX_NAME_LENGTH} character(s)")
        # Return the validated value
        return value
    
    # Custom field validator for 'description'
    # This validator is triggered only when the `description` field is explicitly provided in the input.
    @field_validator("description")
    def validate_description(cls, value):
        # If the field is provided (i.e., not None), perform validation
        if value is not None:
            # Validate that the description meets the minimum length requirement
            if len(value.strip()) < MIN_DESCRIPTION_LENGTH:
                raise ValueError(f"Description must be at least {MIN_DESCRIPTION_LENGTH} character(s)")
            # Validate that the description does not exceed the maximum length
            if len(value) > MAX_DESCRIPTION_LENGTH:
                raise ValueError(f"Description must not exceed {MAX_DESCRIPTION_LENGTH} character(s)")
        # Return the validated value
        return value
