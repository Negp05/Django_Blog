release: python manage.py collectstatic --noinput 
web: gunicorn blog.wsgi:application --bind 0.0.0.0:$PORT 
