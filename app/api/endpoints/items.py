from fastapi import APIRouter, HTTPException, status, Query
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.crud.item import create_item, get_items, get_item_by_id, update_item, delete_item
from typing import List

router = APIRouter()

@router.post("/", response_model=ItemResponse)
async def create_item_endpoint(item: ItemCreate):
    """
    Create a new item.

    - **name**: The name of the item.
    - **description**: A detailed description of the item.
    
    Returns:
    - The created item including the `id`, `name`, and `description`.

    Raises:
    - **400 Bad Request**: If the item creation fails due to any unexpected errors.
    """
    try:
        created_item = await create_item(item)
        return created_item
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create item: {str(e)}"
        )


@router.get("/", response_model=List[ItemResponse])
async def read_items_endpoint(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    """
    Retrieve paginated items.

    Query Parameters:
    - **limit** (optional, default=10): The number of items to retrieve.
    - **offset** (optional, default=0): The starting point in the collection to retrieve items from.

    Returns:
    - A list of items, each including the `id`, `name`, and `description`.
    """
    items = await get_items(limit=limit, offset=offset)
    return items


@router.get("/{id}", response_model=ItemResponse)
async def read_item_endpoint(id: int):
    """
    Retrieve a specific item by its ID.

    - **id**: The ID of the item to retrieve.

    Returns:
    - The item with the specified ID, including the `id`, `name`, and `description`.

    Raises:
    - **404 Not Found**: If the item with the specified ID does not exist.
    """
    item = await get_item_by_id(id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{id}", response_model=ItemResponse)
async def update_item_endpoint(id: int, item_update: ItemUpdate):
    """
    Update an existing item.

    - **id**: The ID of the item to update.
    - **name** (optional): The updated name of the item.
    - **description** (optional): The updated description of the item.

    Returns:
    - The updated item with the new `name` and/or `description`.

    Raises:
    - **404 Not Found**: If the item with the specified ID does not exist.
    - **422 Unprocessable Entity**: If the name or description is empty.
    - **500 Internal Server Error**: If the item could not be updated for unknown reasons.
    """
    existing_item = await get_item_by_id(id)
    if not existing_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    updated_data = item_update.model_dump(exclude_unset=True)
    try:
        updated_item = await update_item(id, item_data=item_update)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update item: {str(e)}")
    
    return updated_item

@router.delete("/{id}")
async def delete_item_endpoint(id: int):
    """
    Delete an existing item by its ID.

    - **id**: The ID of the item to delete.

    Returns:
    - A success message confirming that the item was deleted.

    Raises:
    - **404 Not Found**: If the item with the specified ID does not exist.
    - **500 Internal Server Error**: If the deletion fails due to a database error or other issue.
    """
    existing_item = await get_item_by_id(id)
    if not existing_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    try:
        print(f"Attempting to delete item with id: {id}")  # Debug print to confirm deletion attempt
        await delete_item(id)
        return {"message": "Item deleted successfully"}
    except Exception as e:
        print(f"Exception caught during deletion: {e}")  # Debug print to see the exception
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete item: {str(e)}")
