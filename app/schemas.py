from pydantic import BaseModel, ConfigDict
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    description: str

    # Include model_config only if you have specific configurations
    # Remove arbitrary_types_allowed if not needed
    model_config = ConfigDict(arbitrary_types_allowed=True)

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

    # Replace class-based Config with model_config
    model_config = ConfigDict(from_attributes=True)

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None