from pydantic import BaseModel, ConfigDict
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    description: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True  # Updated from orm_mode

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
