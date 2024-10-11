# app/crud.py

from app.models import Item
from typing import Optional, List

async def create_item(name: str, description: str) -> Item:
    item = await Item.create(name=name, description=description)
    return item

async def get_items() -> List[Item]:
    return await Item.all()

async def get_item_by_id(item_id: int) -> Optional[Item]:
    return await Item.get_or_none(id=item_id)

async def update_item(item_id: int, name: str, description: str) -> Optional[Item]:
    item = await Item.get_or_none(id=item_id)
    if item:
        item.name = name
        item.description = description
        await item.save()
        return item
    return None

async def delete_item(item_id: int) -> bool:
    item = await Item.get_or_none(id=item_id)
    if item:
        await item.delete()
        return True
    return False
