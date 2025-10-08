release: python manage.py este_comando_no_existe
web: python manage.py collectstatic --noinput && gunicorn blog.wsgi:application --bind 0.0.0.0:$PORT

