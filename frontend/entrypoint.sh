#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files (only needed if serving static files from Django)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Start the Django development server
echo "Starting server..."
exec "$@"
