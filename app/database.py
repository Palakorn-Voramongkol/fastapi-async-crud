# app/database.py
from tortoise import Tortoise

async def init_db(db_url: str = 'sqlite://./example.db') -> None:
    """
    Initialize the database connection and generate schemas.

    Args:
        db_url (str): The database URL to connect to. Defaults to an SQLite database at './example.db'.
    
    This function initializes the connection to the database using the specified `db_url` and generates
    the necessary database schemas based on the defined models.
    """
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['app.db.models']}
    )
    await Tortoise.generate_schemas()

async def close_db() -> None:
    """
    Close all active database connections.

    This function is responsible for properly closing all active database connections
    when the application shuts down to prevent resource leaks.
    """
    await Tortoise.close_connections()
