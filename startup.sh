#!/bin/bash
set -e
python manage.py createcachetable
python manage.py migrate --noinput

python manage.py shell -c "
from wagtail.models import Page
if Page.objects.count() <= 2:
    from django.core.management import call_command
    call_command('loaddata', 'fixtures/demo.json', ignorenonexistent=True)
    print('Fixtures loaded!')
else:
    print('Database already has data, skipping fixtures.')
"

python manage.py createsuperuser --noinput --username \$DJANGO_SUPERUSER_USERNAME --email \$DJANGO_SUPERUSER_EMAIL || true

gunicorn myproject.wsgi:application --bind 0.0.0.0:\$PORT