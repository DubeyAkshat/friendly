#!/bin/sh

echo "Waiting for database connection..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "Database connected"

exec "$@"