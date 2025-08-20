release: python backend/manage.py migrate
web: cd backend && gunicorn blog_backend.wsgi:application --bind 0.0.0.0:$PORT
