FROM python

FROM selenium/standalone-firefox

FROM ubuntu:latest

USER root

RUN mkdir -p /usr/src/bot/

WORKDIR /usr/src/bot/

COPY . /usr/src/bot/

RUN set -xe \
    && apt-get update \
    && apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install selenium

RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

EXPOSE 4444