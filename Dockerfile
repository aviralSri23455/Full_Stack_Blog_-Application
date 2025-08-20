# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Collect static files
RUN cd backend && python manage.py collectstatic --noinput || echo "Static files collection skipped"

# Expose port
EXPOSE $PORT

# Start command
CMD cd backend && python manage.py migrate --noinput && gunicorn blog_backend.wsgi:application --bind 0.0.0.0:$PORT
