from pydantic import BaseModel, constr, ConfigDict, Field, ValidationError, field_validator
from typing import Optional
from app.utils.constants import MAX_DESCRIPTION_LENGTH, MAX_NAME_LENGTH, MIN_DESCRIPTION_LENGTH, MIN_NAME_LENGTH

class ItemCreate(BaseModel):
    """
    Pydantic model for creating a new item with custom validation error messages.

    Attributes:
        name (str): The name of the item to be created (non-empty, with length constraints).
        description (str): A detailed description of the item (non-empty, with length constraints).
    """
    
    # Use Field to define the name and description with no length validation here, it will be done in validators
    name: str 
    description: str

    # Custom field validator for 'name'
    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        """
        Validate the 'name' field.

        Ensures that the name has a minimum length of MIN_NAME_LENGTH and 
        does not exceed MAX_NAME_LENGTH.

        Raises:
            ValueError: If the length constraints are not met.

        Returns:
            str: The validated name.
        """
        if len(value) < MIN_NAME_LENGTH:
            raise ValueError(f"Name must be at least {MIN_NAME_LENGTH} character(s)")
        if len(value) > MAX_NAME_LENGTH:
            raise ValueError(f"Name must not exceed {MAX_NAME_LENGTH} character(s)")
        return value
    
    # Custom field validator for 'description'
    @field_validator("description")
    def validate_description(cls, value: str) -> str:
        """
        Validate the 'description' field.

        Strips leading/trailing spaces from the description and ensures that it has 
        a minimum length of MIN_DESCRIPTION_LENGTH and does not exceed MAX_DESCRIPTION_LENGTH.

        Raises:
            ValueError: If the length constraints are not met.

        Returns:
            str: The validated description.
        """
        if len(value.strip()) < MIN_DESCRIPTION_LENGTH:
            raise ValueError(f"Description must be at least {MIN_DESCRIPTION_LENGTH} character(s)")
        if len(value) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Description must not exceed {MAX_DESCRIPTION_LENGTH} character(s)")
        return value


class ItemResponse(BaseModel):
    """
    Pydantic model for returning an item in API responses.

    Attributes:
        id (int): The unique identifier of the item.
        name (str): The name of the item.
        description (str): A detailed description of the item.

    Configuration:
        model_config (ConfigDict): Enables population of the model directly from database attributes.
    """

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
    
    name: Optional[str] = None
    description: Optional[str] = None

    # Custom field validator for 'name'
    @field_validator("name")
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        """
        Validate the 'name' field if provided.

        Ensures that the name, if provided, has a minimum length of MIN_NAME_LENGTH and 
        does not exceed MAX_NAME_LENGTH.

        Raises:
            ValueError: If the length constraints are not met.

        Returns:
            Optional[str]: The validated name or None.
        """
        if value is not None:
            if len(value.strip()) < MIN_NAME_LENGTH:
                raise ValueError(f"Name must be at least {MIN_NAME_LENGTH} character(s)")
            if len(value) > MAX_NAME_LENGTH:
                raise ValueError(f"Name must not exceed {MAX_NAME_LENGTH} character(s)")
        return value
    
    # Custom field validator for 'description'
    @field_validator("description")
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        """
        Validate the 'description' field if provided.

        Strips leading/trailing spaces from the description and ensures that it has a minimum length 
        of MIN_DESCRIPTION_LENGTH and does not exceed MAX_DESCRIPTION_LENGTH.

        Raises:
            ValueError: If the length constraints are not met.

        Returns:
            Optional[str]: The validated description or None.
        """
        if value is not None:
            if len(value.strip()) < MIN_DESCRIPTION_LENGTH:
                raise ValueError(f"Description must be at least {MIN_DESCRIPTION_LENGTH} character(s)")
            if len(value) > MAX_DESCRIPTION_LENGTH:
                raise ValueError(f"Description must not exceed {MAX_DESCRIPTION_LENGTH} character(s)")
        return value
