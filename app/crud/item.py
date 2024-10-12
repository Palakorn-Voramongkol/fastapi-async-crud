# app/crud.py

from app.db.models import Item
from typing import Optional, List
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.utils.exceptions import handle_exceptions, ItemNotFoundError

class ItemError(Exception):
    """Custom Exception for Item CRUD operations."""
    pass

@handle_exceptions
async def create_item(item_data: ItemCreate) -> Item:
    """
    Create a new item in the database.

    Args:
        item_data (ItemCreate): Pydantic model containing the name and description of the item.

    Returns:
        Item: The created Item object.

    Raises:
        ItemError: If the item creation fails unexpectedly.
    """
    try:
        return await Item.create(name=item_data.name, description=item_data.description)
    except Exception as e:
        raise ItemError(f"Failed to create item: {str(e)}")


@handle_exceptions
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



@handle_exceptions
async def get_item_by_id(item_id: int) -> Item:
    """
    Retrieve a single item by its ID.

    Args:
        item_id (int): The ID of the item to retrieve.

    Returns:
        Item: The item with the given ID.

    Raises:
        ItemNotFoundError: If the item with the given ID does not exist.
        ItemError: If a general error occurs during retrieval.
    """
    try:
        item = await Item.get_or_none(id=item_id)
        if not item:
            raise ItemNotFoundError(f"Item with ID {item_id} not found.")
        return item
    except Exception as e:
        raise ItemError(f"Failed to retrieve item by ID {item_id}: {str(e)}")


@handle_exceptions
async def update_item(item_id: int, item_data: ItemUpdate) -> Optional[Item]:
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
        if item_data.name is not None:
            item.name = item_data.name.strip()
        if item_data.description is not None:
            item.description = item_data.description.strip()

        await item.save()
        return item
    else:
        raise ItemNotFoundError(f"Item with ID {item_id} not found.")


async def delete_item(item_id: int) -> bool:
    """
    Deletes an item by ID.
    
    Returns:
    - True if the item is successfully deleted.
    
    Raises:
    - ItemNotFoundError if the item does not exist.
    - ItemError for other database issues.
    """
    try:
        item = await Item.get_or_none(id=item_id)
        if item is None:
            raise ItemNotFoundError(f"Item with ID {item_id} not found.")
        await item.delete()
        return True
    except ItemNotFoundError:
        raise  # Let the ItemNotFoundError propagate
    except Exception as e:
        raise ItemError(f"Failed to delete item with ID {item_id}: {str(e)}")

