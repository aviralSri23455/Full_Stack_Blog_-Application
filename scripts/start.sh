#!/bin/bash
set -e

echo "Starting deployment..."
cd backend

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Static files collection skipped"

echo "Starting gunicorn server..."
exec gunicorn blog_backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2
