#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

echo "Postgres started"

python manage.py collectstatic --noinput
python manage.py migrate --noinput
uwsgi --strict --ini uwsgi.ini

exec "$@"