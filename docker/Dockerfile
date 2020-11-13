FROM amazonlinux:latest

FROM python:3.7-slim

COPY . /srv/flask_app
WORKDIR /srv/flask_app

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

RUN pip install uwsgi

RUN pip install -r requirements.txt --src /usr/local/src

COPY docker/nginx.conf /etc/nginx
RUN chmod +x docker/start.sh
CMD ["docker/start.sh"]