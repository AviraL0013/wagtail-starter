FROM python:3.12-slim as production

ENV VIRTUAL_ENV=/venv

RUN useradd wagtail --create-home && mkdir /app $VIRTUAL_ENV && chown -R wagtail /app $VIRTUAL_ENV

WORKDIR /app

ENV PATH=$VIRTUAL_ENV/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=myproject.settings.production \
    PORT=8000

EXPOSE 8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    && apt-get autoremove && rm -rf /var/lib/apt/lists/*

USER wagtail

RUN python -m venv $VIRTUAL_ENV
COPY requirements.txt ./
RUN pip install --no-cache -r requirements.txt

COPY --chown=wagtail . .

RUN SECRET_KEY=none python manage.py collectstatic --noinput --clear

CMD set -xe; python manage.py createcachetable; python manage.py migrate --noinput; python manage.py loaddata fixtures/demo.json; gunicorn myproject.wsgi:application