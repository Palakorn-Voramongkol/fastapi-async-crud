# app/crud.py

from app.db.models import Item
from typing import Optional, List

class ItemError(Exception):
    """Custom Exception for Item CRUD operations."""
    pass

async def create_item(name: str, description: str) -> Item:
    """
    Create a new item in the database.

    Args:
        name (str): The name of the item.
        description (str): The description of the item.

    Returns:
        Item: The created Item object.

    Raises:
        ValueError: If the name or description is empty.
        ItemError: If the item creation fails unexpectedly.
    """
    if not name:
        raise ValueError("Name cannot be empty.")
    if not description:
        raise ValueError("Description cannot be empty.")
    
    try:
        item = await Item.create(name=name, description=description)
    except Exception as e:
        raise ItemError(f"Failed to create item: {str(e)}")
    
    return item


async def get_items(limit: int = 10, offset: int = 0) -> List[Item]:
    """
    Retrieve a paginated list of items from the database.

    Args:
        limit (int): The maximum number of items to return (default is 10).
        offset (int): The number of items to skip before starting to collect the result set (default is 0).

    Returns:
        List[Item]: A list of Item objects in the database, limited by pagination parameters.
    """
    try:
        return await Item.all().offset(offset).limit(limit)
    except Exception as e:
        raise ItemError(f"Failed to retrieve items: {str(e)}")


async def get_item_by_id(item_id: int) -> Optional[Item]:
    """
    Retrieve a single item by its ID.

    Args:
        item_id (int): The ID of the item to retrieve.

    Returns:
        Optional[Item]: The Item object if found, otherwise None.

    Raises:
        ItemError: If the retrieval process encounters an error.
    """
    try:
        return await Item.get_or_none(id=item_id)
    except Exception as e:
        raise ItemError(f"Failed to retrieve item by ID {item_id}: {str(e)}")


async def update_item(item_id: int, **updates) -> Optional[Item]:
    """
    Update fields of an item dynamically in the database.

    Args:
        item_id (int): The ID of the item to update.
        updates (dict): A dictionary of fields to update, such as name and description.

    Returns:
        Optional[Item]: The updated item, or None if the item was not found.

    Raises:
        ValueError: If the name or description is empty.
        ItemError: If the update process fails unexpectedly.
    """
    item = await Item.get_or_none(id=item_id)
    
    if item:
        # Check for empty 'name' or 'description' and raise ValueError
        if 'name' in updates and not updates['name'].strip():
            raise ValueError("Name cannot be empty.")
        if 'description' in updates and not updates['description'].strip():
            raise ValueError("Description cannot be empty.")

        # Update only fields that are provided (not None)
        try:
            for field, value in updates.items():
                if value is not None:
                    setattr(item, field, value)
            await item.save()
            return item
        except Exception as e:
            raise ItemError(f"Failed to update item with ID {item_id}: {str(e)}")
    else:
        return None


async def delete_item(item_id: int) -> bool:
    """
    Delete an item by its ID.

    Args:
        item_id (int): The ID of the item to delete.

    Returns:
        bool: True if the item was found and deleted, otherwise False.

    Raises:
        ItemError: If the deletion process fails unexpectedly.
    """
    try:
        item = await Item.get_or_none(id=item_id)
        if item:
            await item.delete()
            return True
        return False
    except Exception as e:
        raise ItemError(f"Failed to delete item with ID {item_id}: {str(e)}")
