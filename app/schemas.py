from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    description: str

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
