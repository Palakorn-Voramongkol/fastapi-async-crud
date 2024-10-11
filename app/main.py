from fastapi import FastAPI, HTTPException, status
from app.schemas import ItemCreate, ItemResponse, ItemUpdate
from app.crud import create_item, get_items, get_item_by_id, update_item, delete_item
from app.database import init_db, close_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event: Initialize the database
    await init_db()
    yield
    # Shutdown event: Close the database connection
    await close_db()

app = FastAPI(lifespan=lifespan)

@app.post("/items", response_model=ItemResponse)
async def create_item_endpoint(item: ItemCreate):
    try:
        created_item = await create_item(item.name, item.description)
        return created_item
    except Exception as e:
        # Handle general exceptions, you could also handle specific exceptions like IntegrityError
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create item: {str(e)}"
        )

@app.get("/items", response_model=list[ItemResponse])
async def read_items():
    return await get_items()

@app.get("/items/{id}", response_model=ItemResponse)
async def read_item(id: int):
    item = await get_item_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{id}", response_model=ItemResponse)
async def update_item_endpoint(id: int, item_update: ItemUpdate):
    existing_item = await get_item_by_id(id)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update fields only if provided
    updated_data = item_update.model_dump(exclude_unset=True)
    updated_item = await update_item(id, **updated_data)
    return updated_item


@app.delete("/items/{id}")
async def delete_item_endpoint(id: int):
    # Check if the item exists
    existing_item = await get_item_by_id(id)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Proceed with deletion
    await delete_item(id)
    return {"message": "Item deleted successfully"}
