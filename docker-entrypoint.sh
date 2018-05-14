#!/bin/bash

./wait-for-it/wait-for-it.sh db:5432 -t 60

if [[ $DEBUG == "true" ]]; then
    python manage.py migrate --noinput
    # HACK: create default admin:admin superuser
    # echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin') if User.objects.filter(username='admin').exists() is False else 'Admin already exists'" | python manage.py shell
    python manage.py runserver 0.0.0.0:8000
else
    # Apply database migrations
    echo "Apply database migrations"
    python3 manage.py migrate --noinput

    echo "Store the static files"
    python manage.py collectstatic --noinput
    # Start server
    echo "Starting server"
    # python3 manage.py runserver 0.0.0.0:8000
    gunicorn autoreseller.wsgi:application -w 2 -b :8000
fi