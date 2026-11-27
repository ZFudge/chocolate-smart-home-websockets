FROM python:3.14-alpine

LABEL org.opencontainers.image.authors="zacheryfudge+docker@gmail.com"

WORKDIR /csm-websockets/
COPY . /csm-websockets/
RUN apk add curl
RUN pip install -r requirements.txt
