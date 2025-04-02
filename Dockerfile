# Use Python base image
FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y libreoffice

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 8080

# Start both Flask app and Celery worker
CMD ["sh", "-c", "celery -A celery_worker worker --loglevel=info & python server.py"]
