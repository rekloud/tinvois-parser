FROM python:3.8-slim

WORKDIR /app

RUN useradd -ms /bin/bash taxapp && \
  apt-get update && apt-get install curl unixodbc-dev gnupg2 --yes

RUN apt-get update &&\
    mkdir ${HOME}/google_auth &&\
    set GOOGLE_APPLICATION_CREDENTIALS=${HOME}/google_atuh

COPY --chown=taxapp app .
RUN pip install -r ./requirements.txt

USER taxapp
CMD [ "python3", "./manage.py"]
