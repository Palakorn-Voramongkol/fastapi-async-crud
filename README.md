# FastAPI Asynchronous CRUD Application

This project is a FastAPI-based application that demonstrates asynchronous CRUD operations using SQLite and Pytest for testing. It follows clean code practices and includes proper test coverage.

## Project Structure

```plaintext
palakorn-fastapi-async-crud/
├── .vscode/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── items.py
│   │   ├── crud/
│   │   │   ├── __init__.py
│   │   │   ├── item.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── item.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── main.py
├── fastapi_env/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_crud_api_items_create.py
│   ├── test_crud_api_items_delete.py
│   ├── test_crud_api_items_read.py
│   ├── test_crud_api_items_update.py
│   ├── test_crud_entity_items_create.py
│   ├── test_crud_entity_items_delete.py
│   ├── test_crud_entity_items_read.py
│   ├── test_crud_entity_items_update.py
│   ├── test_database.py
│   ├── test_lifespan.py
│   ├── test_schema_items.py
├── .coverage
├── .coveragerc
├── .gitignore
├── environment.yml
├── example.db
├── pytest.ini
├── README.md
├── requirements.txt
```

## Directories and Files

### 1. `app/`
Contains the core application logic.

- **api/endpoints/**: Contains the FastAPI endpoints for CRUD operations on items.
  - `items.py`: Defines the CRUD routes for items.
  
- **api/crud/**: Contains the CRUD functionality, including database interactions.
  - `item.py`: Functions for creating, reading, updating, and deleting items in the database.
  
- **api/db/**: Database connection and models.
  - `models.py`: Defines the database models using SQLite.
  
- **schemas/**: Defines the Pydantic models used for data validation and serialization.
  - `item.py`: Contains the schema for `Item` and its properties.

- **utils/**: Utility functions, including database connection setup and the main application entry point.
  - `database.py`: Handles the asynchronous database connection.
  - `main.py`: Main entry point to start the FastAPI application.

### 2. `tests/`
Contains the test cases for the application.

- **test_crud_api_items_*.py**: Tests for CRUD API endpoints for `Item` creation, deletion, reading, and updating.
- **test_crud_entity_items_*.py**: Entity-level tests for CRUD operations on items.
- **test_database.py**: Test cases for database operations.
- **test_lifespan.py**: Tests related to application lifespan events (startup/shutdown).
- **test_schema_items.py**: Schema validation tests for the `Item` model.


### 3. `environment.yml`
Environment file for setting up dependencies using Conda.

### 4. `requirements.txt`
Lists the required Python dependencies for the project.

### 5. `.coveragerc`
Configuration file for test coverage.

### 6. `pytest.ini`
Configuration file for Pytest, including plugins and async mode settings.

## Setup Instructions

### 1. Create Virtual Environment

You can create a virtual environment for the project using Conda:

```bash
conda env create -f environment.yml
conda activate fastapi_env
```

Alternatively, using `venv`:

```bash
python3 -m venv fastapi_env
source fastapi_env/bin/activate  # On Windows: fastapi_env\Scripts\activate
```

### 2. Install Dependencies

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

To start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

This will run the server on `http://127.0.0.1:8000`.


### 4. Run the Tests

To run the tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

You can also specify `-s` for additional print output:

```bash
pytest --cov=app --cov-report=term-missing -s
```

## Testing

- **Unit Tests**: Test CRUD operations and other application logic.
- **Coverage**: Ensure test coverage using Pytest's coverage plugin.

## Author

This project is created and maintained by **Palakorn Voramongkol**.
