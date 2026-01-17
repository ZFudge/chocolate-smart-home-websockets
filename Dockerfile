FROM python:3.13-alpine

LABEL org.opencontainers.image.authors="zacheryfudge+docker@gmail.com"

WORKDIR /ws-service/
COPY requirements.txt /ws-service/
RUN mkdir -p /var/logs/ws-service/

RUN apk add gcc python3-dev
RUN pip install -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:ws-service"

EXPOSE 8001
