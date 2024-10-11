from pydantic import BaseModel, constr, ConfigDict, Field
from typing import Optional
from app.utils.constants import MAX_DESCRIPTION_LENGTH, MAX_NAME_LENGTH, MIN_DESCRIPTION_LENGTH, MIN_NAME_LENGTH

class ItemCreate(BaseModel):
    """
    Pydantic model for creating a new item.

    Attributes:
        name (str): The name of the item to be created (non-empty).
        description (str): A detailed description of the item (non-empty).
    
    Configuration:
        model_config (ConfigDict): Configuration for Pydantic model.
    """
    
    # Ensures that both 'name' and 'description' are non-empty strings
    # Enforce min and max length on name and description using Field
    name: str = Field(..., min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: str = Field(..., min_length=MIN_DESCRIPTION_LENGTH, max_length=MAX_DESCRIPTION_LENGTH)


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

    # These are optional fields, but length constraints are enforced if provided
    name: Optional[str] = Field(None, min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: Optional[str] = Field(None, min_length=MIN_DESCRIPTION_LENGTH, max_length=MAX_DESCRIPTION_LENGTH)
