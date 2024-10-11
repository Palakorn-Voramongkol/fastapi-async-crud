import pytest
import pytest_asyncio
from app.database import init_db, close_db
from tortoise.exceptions import OperationalError, ConfigurationError
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_init_db():
    await init_db(db_url='sqlite://:memory:')
    # Perform a simple database operation to confirm connectivity
    from app.models import Item
    try:
        items = await Item.all()
    except Exception as e:
        pytest.fail(f"Database operation failed after initialization: {e}")
    await close_db()

@pytest.mark.asyncio
async def test_close_db():
    await init_db(db_url='sqlite://:memory:')
    await close_db()
    # Use mocking to confirm that close_connections() is called
    with patch('tortoise.Tortoise.close_connections', new_callable=AsyncMock) as mock_close:
        await close_db()
        mock_close.assert_awaited_once()
