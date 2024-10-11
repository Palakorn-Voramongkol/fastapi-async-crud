import pytest
import asyncio
from tortoise.contrib.test import initializer, finalizer
from app.main import app

@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module", autouse=True)
def initialize_db(event_loop, request):
    # Initialize the test database with models
    initializer(['app.models'], db_url="sqlite://:memory:", app_label="models")
    # Register the finalizer to run within the event loop
    def teardown():
        event_loop.run_until_complete(finalizer())
    request.addfinalizer(teardown)
