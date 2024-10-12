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
    
# Use Field to define min and max length
    name: str 
    description: str 

    # Custom field validator for name
    @field_validator("name")
    def validate_name(cls, value):
        print("*******************")
        print(value)
        if len(value) < MIN_NAME_LENGTH:
            raise ValueError(f"Name must be at least {MIN_NAME_LENGTH} characters long.")
        if len(value) > MAX_NAME_LENGTH:
            raise ValueError(f"Name must not exceed {MAX_NAME_LENGTH} characters.")
        return value
    
    # Custom field validator for description
    @field_validator("description")
    def validate_description(cls, value):
        if len(value.strip()) < MIN_DESCRIPTION_LENGTH:
            raise ValueError(f"Description must be at least {MIN_DESCRIPTION_LENGTH} characters long.")
        if len(value) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Description must not exceed {MAX_DESCRIPTION_LENGTH} characters.")
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

    id: int
    name: str
    description: str

    # Model configuration to enable attribute population from DB models
    model_config = ConfigDict(from_attributes=True)


class ItemUpdate(BaseModel):
    """
    Pydantic model for updating an existing item.

    Attributes:
        name (Optional[str]): The updated name of the item (optional, can be omitted).
        description (Optional[str]): The updated description of the item (optional, can be omitted).
    """
    
    name: Optional[str] = None
    description: Optional[str] = None

    # Custom field validator for name
    @field_validator("name")
    def validate_name(cls, value):
        if (value != None):
            if len(value.strip()) < MIN_NAME_LENGTH:
                raise ValueError(f"Name must be at least {MIN_NAME_LENGTH} characters long.")
            if len(value) > MAX_NAME_LENGTH:
                raise ValueError(f"Name must not exceed {MAX_NAME_LENGTH} characters.")
            return value
    
    # Custom field validator for description
    @field_validator("description")
    def validate_description(cls, value):
        if (value != None):
            if len(value.strip()) < MIN_DESCRIPTION_LENGTH:
                raise ValueError(f"Description must be at least {MIN_DESCRIPTION_LENGTH} characters long.")
            if len(value) > MAX_DESCRIPTION_LENGTH:
                raise ValueError(f"Description must not exceed {MAX_DESCRIPTION_LENGTH} characters.")
            return value
