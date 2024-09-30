#!/usr/bin/env bash
# wait-for-it.sh: wait until a service is ready


while ! nc -z db 5432; do   
  echo "Waiting for the PostgreSQL database..."
  sleep 2
done

echo "PostgreSQL is up!"
exec "$@"

