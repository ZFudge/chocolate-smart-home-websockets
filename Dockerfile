FROM python:3.14-alpine

LABEL org.opencontainers.image.authors="zacheryfudge+docker@gmail.com"

WORKDIR /ws-service/
COPY requirements.txt /ws-service/
RUN mkdir -p /var/logs/ws-service/

RUN pip install -r requirements.txt
RUN apk add curl
