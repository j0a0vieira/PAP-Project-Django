web: gunicorn src.wsgi --log-file -
web: python manage.py collectstatic --no-input; gunicorn src.wsgi --log-file - --log-level debug
web: python manage.py makemigrations --no-input
web: python manage.py migrate --no-input