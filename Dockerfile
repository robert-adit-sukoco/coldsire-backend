# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Define the command to run your FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
