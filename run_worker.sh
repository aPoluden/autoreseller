#!/bin/bash

./wait-for-it/wait-for-it.sh db:5432 -t 60
celery -A autoreseller worker -B -l debug