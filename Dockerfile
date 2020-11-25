FROM python:3.8-slim-buster

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
        build-essential imagemagick libpq-dev libxslt1-dev npm \
        libjpeg-dev poppler-utils libffi-dev \
    && ln -sf /usr/bin/nodejs /usr/local/bin/node \
    && npm install -g less

RUN useradd --create-home web
WORKDIR /home/web
USER web

COPY wsgi.py pyproject.toml poetry.lock README.md ./
ADD extranet /home/web/extranet
ADD tests /home/web/tests

RUN poetry install --no-dev

ENV FLASK_SECRET_KEY topsecret
ENV SECRET_KEY topsecret
EXPOSE 5000

CMD [ "poetry", "run", "flask", "run" ]
