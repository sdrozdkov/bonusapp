FROM python:3.6-stretch
# FROM ubuntu:16.04

ENV LANG='C.UTF-8' LC_ALL='C.UTF-8'

COPY . /srv/flask-full
WORKDIR /srv/flask-full

RUN apt-get update --fix-missing \
    && apt-get install --no-install-recommends -y locales git bash python3-pip build-essential libssl-dev libffi-dev \
    && locale-gen en_US.UTF-8 \
    && apt-get -o Dpkg::Options::="--force-confmiss" install --reinstall -y netbase \
    && pip3 install --no-cache-dir --upgrade pip setuptools \
    && pip3 install --no-cache-dir -r requirements.txt \
    && pip3 install --no-cache-dir -r requirements_test.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
