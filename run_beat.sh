#!/bin/sh

./wait-for-it/wait-for-it.sh db:5432 -t 60
celery -A autoreseller beat -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler