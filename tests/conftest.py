# tests/conftest.py
import pytest_asyncio
from tortoise import Tortoise

@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_db():
    # Initialize the Tortoise ORM
    await Tortoise.init(
        db_url='sqlite://:memory:',
        modules={'models': ['app.models']}
    )
    # Generate the database schema
    await Tortoise.generate_schemas()
    yield
    # Close all connections after tests
    await Tortoise.close_connections()
