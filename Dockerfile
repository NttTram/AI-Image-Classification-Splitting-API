# # Use an official Python runtime as a parent image
# FROM python:3.9-slim

# # Set the working directory in the container
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libffi-dev \
#     libssl-dev

# # Update pip
# RUN pip install --upgrade pip

# # Copy only the requirements file first to leverage Docker cache
# ADD ./app/requirements.txt /app/requirements.txt

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application
# COPY ./app /app

# # Make port 8000 available to the world outside the container
# EXPOSE 8000

# # Define environment variable
# ENV NAME=World

# # Run app.py when the container launches
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Choose a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the Docker image
COPY ./app /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]