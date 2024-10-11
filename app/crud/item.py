# app/crud.py

from app.models import Item
from typing import Optional, List

async def create_item(name: str, description: str) -> Item:
    """
    Create a new item in the database.

    Args:
        name (str): The name of the item.
        description (str): The description of the item.

    Returns:
        Item: The created Item object.
    """
    item = await Item.create(name=name, description=description)
    return item

async def get_items() -> List[Item]:
    """
    Retrieve all items from the database.

    Returns:
        List[Item]: A list of all Item objects in the database.
    """
    return await Item.all()

async def get_item_by_id(item_id: int) -> Optional[Item]:
    """
    Retrieve a single item by its ID.

    Args:
        item_id (int): The ID of the item to retrieve.

    Returns:
        Optional[Item]: The Item object if found, otherwise None.
    """
    return await Item.get_or_none(id=item_id)


async def update_item(item_id: int, **updates) -> Optional[Item]:
    """
    Update fields of an item dynamically in the database.

    Args:
        item_id (int): The ID of the item to update.
        updates (dict): A dictionary of fields to update, such as name and description.

    Returns:
        Optional[Item]: The updated item, or None if the item was not found.
    """
    item = await Item.get_or_none(id=item_id)
    if item:
        # Filter out None values and update only the fields passed
        for field, value in updates.items():
            if value is not None:
                setattr(item, field, value)
        await item.save()
        return item
    return None



async def delete_item(item_id: int) -> bool:
    """
    Delete an item by its ID.

    Args:
        item_id (int): The ID of the item to delete.

    Returns:
        bool: True if the item was found and deleted, otherwise False.
    """
    item = await Item.get_or_none(id=item_id)
    if item:
        await item.delete()
        return True
    return False
