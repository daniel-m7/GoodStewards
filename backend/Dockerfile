# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to prevent writing .pyc files and to run in unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Copy only the files necessary for dependency installation to leverage Docker cache
COPY pyproject.toml poetry.lock* ./

# Configure poetry and install dependencies
# Do not create a virtual environment in the container
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY ./app ./app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
