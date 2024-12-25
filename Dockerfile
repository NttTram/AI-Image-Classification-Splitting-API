# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
ADD ./app/requirements.txt /app/requirements.txt

# Install any needed packages specified inn requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ./app /app

# Make port 8000 available to the world outside the container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]