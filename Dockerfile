FROM python:3.8-slim

WORKDIR /app

RUN useradd -ms /bin/bash taxapp && \
  apt-get update && apt-get install curl unixodbc-dev gnupg2 --yes

RUN apt-get update
RUN apt-get install nano

COPY --chown=taxapp app .
RUN mkdir google_auth
RUN pip install -r ./requirements.txt

USER taxapp
CMD ["python3", "./manage.py"]
