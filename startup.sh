#!/bin/bash
set -e
python manage.py createcachetable
python manage.py migrate --noinput
python manage.py shell -c "
from wagtail.models import Page
if Page.objects.count() <= 2:
    import subprocess
    subprocess.run(['python', 'manage.py', 'loaddata', 'fixtures/demo.json'], check=True)
    print('Fixtures loaded!')
else:
    print('Database already has data, skipping fixtures.')
"
python manage.py shell -c "from wagtail.images.models import Rendition; Rendition.objects.all().delete()"
gunicorn myproject.wsgi:application