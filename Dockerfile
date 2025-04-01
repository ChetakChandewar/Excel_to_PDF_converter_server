# Use a lightweight Python image
FROM python:3.9

# Install LibreOffice CLI
RUN apt-get update && apt-get install -y libreoffice && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy project files
COPY server.py requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Start the Flask app
CMD ["python", "server.py"]
