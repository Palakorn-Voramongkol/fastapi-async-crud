from app.models import Item

async def create_item(name: str, description: str):
    return await Item.create(name=name, description=description)

async def get_items():
    return await Item.all()

async def get_item_by_id(item_id: int):
    return await Item.get(id=item_id)

async def update_item(item_id: int, name: str, description: str):
    item = await Item.get(id=item_id)
    item.name = name
    item.description = description
    await item.save()
    return item

async def delete_item(item_id: int):
    await Item.filter(id=item_id).delete()
