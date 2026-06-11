FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY config.py .
COPY database.py .
COPY questions.py .
COPY utils.py .
COPY .env .

# Create data directory
RUN mkdir -p /data

# Run the bot
CMD ["python", "main.py"]