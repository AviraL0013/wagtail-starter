#!/bin/bash
set -e
python manage.py createcachetable
python manage.py migrate --noinput
python manage.py loaddata fixtures/demo.json
python manage.py shell -c "from wagtail.images.models import Rendition; Rendition.objects.all().delete()"
gunicorn myproject.wsgi:application