# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and the Python script
COPY requirements.txt ./
COPY file_watcher.py ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file to the working directory
COPY .env .env

# Run the Python script
CMD ["python", "file_watcher.py"]
