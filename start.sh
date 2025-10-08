#!/bin/bash
python manage.py migrate
gunicorn Django_Blog.wsgi --bind 0.0.0.0:$PORT