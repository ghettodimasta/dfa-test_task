# syntax=docker/dockerfile:1
FROM ubuntu:20.04
ENV LANG en_US.UTF-8
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /dfa
COPY ./ /dfa
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install libpq-dev
RUN apt install -y python3-pip python3.9-dev
RUN apt-get install libgdal-dev -y
RUN python3 -m pip install pipenv
RUN pipenv install
ENV PYTHONPATH "/dfa"
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]