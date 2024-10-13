# Use the official Python image as a base
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install pytest as a development dependency
RUN pip install pytest

# Copy the entire application code to the container
COPY . .

# Expose the port that the app runs on
EXPOSE 8000

# Default command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Optionally, you can add a separate entry point for testing
# You can use an ARG to specify whether to run the tests or the application
ARG RUN_TESTS=false

# If RUN_TESTS is true, run pytest instead of the application
CMD if [ "$RUN_TESTS" = "true" ]; then pytest --maxfail=1 --disable-warnings -v; else uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload; fi
