#FROM python:3.8-slim
FROM tiangolo/meinheld-gunicorn-flask:python3.8

WORKDIR /app

RUN useradd -ms /bin/bash taxapp && \
  apt-get update && apt-get install curl unixodbc-dev gnupg2 --yes

RUN apt-get install nano && \
    apt-get install libgl1-mesa-glx --yes

COPY --chown=taxapp app .
RUN mkdir -p google_auth
RUN pip install -r ./requirements.txt

USER taxapp
