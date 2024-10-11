from fastapi import APIRouter, HTTPException, status
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.crud.item import create_item, get_items, get_item_by_id, update_item, delete_item

router = APIRouter()

@router.post("/", response_model=ItemResponse)
async def create_item_endpoint(item: ItemCreate):
    try:
        created_item = await create_item(item.name, item.description)
        return created_item
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create item: {str(e)}"
        )

@router.get("/", response_model=list[ItemResponse])
async def read_items():
    return await get_items()

@router.get("/{id}", response_model=ItemResponse)
async def read_item(id: int):
    item = await get_item_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{id}", response_model=ItemResponse)
async def update_item_endpoint(id: int, item_update: ItemUpdate):
    existing_item = await get_item_by_id(id)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_data = item_update.model_dump(exclude_unset=True)
    updated_item = await update_item(id, **updated_data)
    return updated_item

@router.delete("/{id}")
async def delete_item_endpoint(id: int):
    existing_item = await get_item_by_id(id)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    await delete_item(id)
    return {"message": "Item deleted successfully"}
