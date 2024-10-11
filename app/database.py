# app/database.py

from tortoise import Tortoise

async def init_db(db_url='sqlite://./example.db'):
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()
