#!/bin/sh

echo "Waiting for database connection..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "Database connected"
    
python manage.py collectstatic --noinput --clear
gunicorn friendly.wsgi:application --bind 0.0.0.0:8000
