from pydantic import BaseModel, constr, ConfigDict
from typing import Optional

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
    name: constr(min_length=1)  # name must be at least 1 character
    description: constr(min_length=1)  # description must be at least 1 character

    # Model configuration for allowing arbitrary types if needed
    model_config = ConfigDict(arbitrary_types_allowed=True)


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
