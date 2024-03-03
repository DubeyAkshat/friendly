#!/bin/sh

echo "Waiting for PostgresSQL connection..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
    echo "Database connected"
    
python manage.py collectstatic --noinput --clear
gunicorn friendly_django.wsgi:application --bind 0.0.0.0:8000 --reload
