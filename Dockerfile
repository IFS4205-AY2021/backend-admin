FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /home/admin /home/admin/app /home/admin/resources
WORKDIR /home/admin

COPY requirements.txt run.sh ./
RUN apt-get install gcc
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*
# RUN apt-get install libevent-dev
RUN pip install graphviz
RUN apt-get install software-properties-common
RUN apt update -y
RUN apt-get install graphviz libgraphviz-dev pkg-config -y
RUN pip install --install-option="--include-path=/usr/local/include/" --install-option="--library-path=/usr/local/lib/" pygraphviz


RUN pip install -r ./requirements.txt
RUN pip install mysql-connector-python
RUN pip install python-dotenv
RUN pip install djangorestframework

# Change environment:
ENV envir=development
COPY ./resources/dev.env ./.env
# ENV envir=production
# COPY ./resources/prd.env ./.env

RUN export $(cat .env)

ENTRYPOINT [ "/bin/bash", "./run.sh" ]
