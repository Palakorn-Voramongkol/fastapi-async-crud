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



## Testing


### Code Coverage: Test CRUD operations and other application logic.

| File                                   | Statements | Missing | Excluded | Coverage |
| -------------------------------------- | ---------- | ------- | -------- | -------- |
| app/api/endpoints/items.py             | 45         | 0       | 0        | 100%     |
| app/crud/item.py                       | 49         | 0       | 0        | 100%     |
| app/database.py                        | 6          | 0       | 0        | 100%     |
| app/db/models.py                       | 7          | 0       | 0        | 100%     |
| app/main.py                            | 11         | 3       | 0        | 73%      |
| app/schemas/item.py                    | 44         | 0       | 0        | 100%     |
| app/utils/constants.py                 | 4          | 0       | 0        | 100%     |
| app/utils/exceptions.py                | 17         | 0       | 0        | 100%     |
| tests/__init__.py                      | 0          | 0       | 0        | 100%     |
| tests/conftest.py                      | 8          | 0       | 0        | 100%     |
| tests/test_crud_api_items_create.py    | 48         | 1       | 0        | 98%      |
| tests/test_crud_api_items_delete.py    | 44         | 0       | 0        | 100%     |
| tests/test_crud_api_items_read.py      | 38         | 0       | 0        | 100%     |
| tests/test_crud_api_items_update.py    | 52         | 1       | 0        | 98%      |
| tests/test_crud_entity_items_create.py | 73         | 4       | 0        | 95%      |
| tests/test_crud_entity_items_delete.py | 48         | 0       | 0        | 100%     |
| tests/test_crud_entity_items_read.py   | 59         | 0       | 0        | 100%     |
| tests/test_crud_entity_items_update.py | 87         | 2       | 0        | 98%      |
| tests/test_database.py                 | 21         | 2       | 0        | 90%      |
| tests/test_lifespan.py                 | 32         | 3       | 0        | 91%      |
| tests/test_schema_items.py             | 39         | 0       | 0        | 100%     |
| **Total**                              | **732**    | **16**  | **0**    | **98%**  |



Install coverage tools:
```bash
pip install pytest pytest-cov coverage
```

To run the tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

You can also specify `-s` for additional print output:

```bash
pytest --cov=app --cov-report=term-missing -s
```


Run tests and generate HTML coverage report:
```bash
pytest --cov=app --cov-report html      
```

Open the report
```bash
open coverage_html_report/index.html 
```
## API Usage

### 1. **Create a New Item**

**Endpoint:**
```http
POST /items/
```

**Description:**
- Creates a new item with the provided name and description.

**Request Body:**
- `name` (string): The name of the item (required).
- `description` (string): A detailed description of the item (required).

**Response:**
- Returns the created item with the following fields:
  - `id`: Unique identifier of the item.
  - `name`: Name of the item.
  - `description`: Description of the item.

**Example:**
```bash
curl -X 'POST' \
  'http://localhost:8000/items/' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Sample Item",
    "description": "This is a sample item"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Sample Item",
  "description": "This is a sample item"
}
```

### 2. **Retrieve Paginated Items**

**Endpoint:**
```http
GET /items/
```

**Description:**
- Retrieves a list of items with pagination.

**Query Parameters:**
- `limit` (integer, optional): Number of items to retrieve (default is 10).
- `offset` (integer, optional): The starting index for retrieving items (default is 0).

**Response:**
- Returns a list of items, each containing:
  - `id`: Unique identifier of the item.
  - `name`: Name of the item.
  - `description`: Description of the item.

**Example:**
```bash
curl -X 'GET' 'http://localhost:8000/items/?limit=5&offset=0'
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Sample Item",
    "description": "This is a sample item"
  },
  ...
]
```

### 3. **Retrieve an Item by ID**

**Endpoint:**
```http
GET /items/{id}
```

**Description:**
- Retrieves a specific item by its unique identifier.

**Path Parameter:**
- `id` (integer): The ID of the item to retrieve.

**Response:**
- Returns the item with the given ID:
  - `id`: Unique identifier of the item.
  - `name`: Name of the item.
  - `description`: Description of the item.

**Example:**
```bash
curl -X 'GET' 'http://localhost:8000/items/1'
```

**Response:**
```json
{
  "id": 1,
  "name": "Sample Item",
  "description": "This is a sample item"
}
```

### 4. **Update an Item**

**Endpoint:**
```http
PUT /items/{id}
```

**Description:**
- Updates an existing item with the given ID. The name or description can be updated.

**Path Parameter:**
- `id` (integer): The ID of the item to update.

**Request Body:**
- `name` (string, optional): Updated name of the item.
- `description` (string, optional): Updated description of the item.

**Response:**
- Returns the updated item with the following fields:
  - `id`: Unique identifier of the item.
  - `name`: Updated name of the item.
  - `description`: Updated description of the item.

**Example:**
```bash
curl -X 'PUT' \
  'http://localhost:8000/items/1' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Updated Item",
    "description": "Updated item description"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Updated Item",
  "description": "Updated item description"
}
```

### 5. **Delete an Item**

**Endpoint:**
```http
DELETE /items/{id}
```

**Description:**
- Deletes an existing item by its ID.

**Path Parameter:**
- `id` (integer): The ID of the item to delete.

**Response:**
- A success message confirming that the item was deleted.

**Example:**
```bash
curl -X 'DELETE' 'http://localhost:8000/items/1'
```

**Response:**
```json
{
  "message": "Item deleted successfully"
}
```


## Author

This project is created and maintained by **Palakorn Voramongkol**.
