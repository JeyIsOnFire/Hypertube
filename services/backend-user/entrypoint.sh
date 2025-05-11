#!/bin/sh

echo "Starting backend-user container..."

echo "⚙️  Running migrations..."
python manage.py migrate --noinput

# python manage.py collectstatic --noinput

echo "🚀 Launching Uvicorn server..."
exec "$@"
