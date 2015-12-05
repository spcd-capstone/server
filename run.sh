#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

cd $DIR

# launch redis server
redis-server ./redis.conf &

# launch celery worker
./venv/bin/celery worker -A hacer.tasks.celery &

./venv/bin/python manage.py runserver

