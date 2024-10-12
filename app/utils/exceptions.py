from functools import wraps
import logging

logger = logging.getLogger(__name__)

class ItemError(Exception):
    """
    Custom Exception for Item CRUD operations.
    """
    pass

class ItemNotFoundError(Exception):
    """
    Raised when an item is not found in the database.
    """
    pass

def handle_exceptions(func):
    """
    Decorator to handle exceptions in CRUD operations.

    Args:
        func (Callable): The CRUD function to wrap with exception handling.

    Returns:
        Callable: The wrapped function.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ItemNotFoundError:
            # Let ItemNotFoundError pass through without modification
            raise
        except Exception as e:
            raise ItemError(f"An error occurred: {str(e)}")
    return wrapper
