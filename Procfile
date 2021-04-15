web: gunicorn src.wsgi --log-file -
web: python manage.py collectstatic --no-input; gunicorn src.wsgi --log-file - --log-level debug
