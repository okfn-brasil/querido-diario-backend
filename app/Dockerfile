FROM docker.io/python:3.9-bullseye

ARG HOME_DIR=/opt/app
ARG UNAME=queridodiario

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$HOME_DIR

RUN useradd --no-log-init --system $UNAME && \
	apt-get update -y && \
  apt-get install -y python3.9-dev wait-for-it

WORKDIR $HOME_DIR

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R $UNAME:$UNAME $HOME_DIR

USER $UNAME
