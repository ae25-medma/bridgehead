# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask
RUN pip install flask

# Make the /data directory
RUN mkdir -p /data

# Expose port 5462 for the Flask server
EXPOSE 5462

# Define the command to run the application
CMD ["python", "upload_server.py"]
