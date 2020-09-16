FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /home/admin /home/admin/app /home/admin/resources
WORKDIR /home/admin

COPY requirements.txt run.sh ./
RUN pip install -r ./requirements.txt

# Change environment:
ENV envir=development
COPY ./resources/dev.env ./.env
# ENV envir=production
# COPY ./resources/prd.env ./.env

RUN export $(cat .env)

ENTRYPOINT [ "/bin/bash", "./run.sh" ]
