#!/usr/bin/env bash
#!/bin/sh

apt-get update && apt-get install -y netcat



python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

exec "$@"