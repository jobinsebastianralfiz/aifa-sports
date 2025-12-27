#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if not exists..."
python manage.py createsuperuser --noinput 2>/dev/null || echo "Superuser already exists or could not be created"

echo "Starting Gunicorn..."
exec gunicorn config.wsgi --bind 0.0.0.0:${PORT:-8000} --log-file -
