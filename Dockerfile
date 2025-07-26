# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
# This is useful for the initial build, but the volume mount will override it during development
COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the app with Gunicorn, enabling hot-reloading for development
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--reload", "src.app:app"]