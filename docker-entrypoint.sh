#!/bin/bash
python src/manage.py makemigrations --no-input
python src/manage.py migrate --no-input
python src/manage.py collectstatic --no-input
exec "$@"