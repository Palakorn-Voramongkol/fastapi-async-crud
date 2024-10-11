import pytest_asyncio
from tortoise import Tortoise

@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_db():
    """
    Fixture to initialize the Tortoise ORM and setup the database for testing.
    
    This fixture is automatically applied for the entire test session and runs before any test cases.
    It performs the following steps:
    
    1. **Initialize Tortoise ORM**: Connects to an in-memory SQLite database using the `db_url` 
       parameter (`sqlite://:memory:`). This means that the database is ephemeral and will not persist between sessions.
    2. **Generate Database Schema**: Automatically creates all necessary tables based on the models 
       specified in the `modules` argument, i.e., models defined in the `'app.models'` module.
    3. **Yield for Test Execution**: Once the database is set up, it yields control to the test functions, 
       allowing them to run their database operations.
    4. **Close Connections After Tests**: After all tests are complete, it closes the database connections, 
       ensuring no resources are left open.
    
    This fixture ensures that the database is properly initialized and torn down, making it an essential part of the testing process.
    
    Attributes:
    - `scope="session"`: The fixture is run once per testing session, ensuring that the database setup 
      only happens once at the start.
    - `autouse=True`: This fixture is automatically applied without needing to be explicitly called in test functions.
    
    Example:
    Any test that interacts with the database will benefit from this fixture as it ensures that the schema 
    is always up-to-date and the database connection is managed properly.
    """
    # Initialize the Tortoise ORM
    await Tortoise.init(
        db_url='sqlite://:memory:',  # In-memory SQLite DB for testing
        modules={'models': ['app.models']}  # Point to the models in 'app.models'
    )
    
    # Generate the database schema (create tables based on models)
    await Tortoise.generate_schemas()
    
    # Yield to allow test functions to run
    yield
    
    # Close all database connections after the tests are done
    await Tortoise.close_connections()
