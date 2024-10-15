from fastapi import FastAPI
from app.database import init_db, close_db
from app.api.endpoints import items  # Import your items endpoint module
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan event handler for FastAPI.

    This function initializes the database on app startup and closes 
    the connection when the app shuts down.
    
    Returns:
        - An asynchronous generator with no values.
    """
    await init_db()  # Startup: Initialize the database
    yield
    await close_db()  # Shutdown: Close the database connection

# Initialize the FastAPI app with lifespan events
app = FastAPI(lifespan=lifespan)

# Include the item endpoints from the refactored items module
app.include_router(items.router, prefix="/items", tags=["items"])
