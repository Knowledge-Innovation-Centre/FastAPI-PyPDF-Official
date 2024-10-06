# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies including GCC and build tools
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    build-essential \
    gcc

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 8081 for the application
EXPOSE 8081

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
