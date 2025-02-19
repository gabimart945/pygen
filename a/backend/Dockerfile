
# Dockerfile for Backend
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . /app

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
        