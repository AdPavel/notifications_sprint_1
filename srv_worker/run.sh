#!/bin/sh

echo "Waiting for rabbit..."

while ! nc -z $RABBIT_HOST $RABBIT_PORT; do
  sleep 3
done

echo "Rabbit started"

python main.py

exec "$@"