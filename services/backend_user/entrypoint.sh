#!/bin/sh

echo "Starting backend_user container..."

echo "⚙️  Running migrations..."
python manage.py makemigrations users

python manage.py migrate

python manage.py showmigrations
# python manage.py collectstatic --noinput

echo "🚀 Launching Uvicorn server..."
exec "$@"
