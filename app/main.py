from fastapi import FastAPI, HTTPException
from app.schemas import ItemCreate, ItemResponse, ItemUpdate
from app.crud import create_item, get_items, get_item_by_id, update_item, delete_item
from app.database import init_db, close_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

@app.post("/items", response_model=ItemResponse)
async def create_item_endpoint(item: ItemCreate):
    return await create_item(item.name, item.description)

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
    updated_data = item_update.dict(exclude_unset=True)
    updated_item = await update_item(id, **updated_data)
    return updated_item

@app.delete("/items/{id}")
async def delete_item_endpoint(id: int):
    await delete_item(id)
    return {"message": "Item deleted successfully"}
