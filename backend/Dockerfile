# Base Image
FROM python:3.11-slim

# Set Working Directory
WORKDIR /app

# Copy Requirements
COPY requirements.txt .

# Install Dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy Application Code
COPY . .

# Generate the BAML client
RUN baml-cli generate

# Expose Port
EXPOSE 8000

# Run Command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
