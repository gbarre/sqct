FROM ubuntu:20.04

MAINTAINER Guillaume Barré "guillaume-sqct@jrmv.net"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY api api
COPY auth.py .
COPY migrations migrations
COPY spec/openapi.yml spec/openapi.yml
COPY app.py .
COPY config.py .
COPY models.py .
COPY server.py .
# COPY entrypoint.sh .

ENTRYPOINT [ "gunicorn" ]
CMD [ "server:app", "--access-logfile", "-", "--error-logfile", "-", "--bind=0.0.0.0:5000", "--workers=1"]