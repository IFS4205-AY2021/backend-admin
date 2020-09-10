FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /home/admin
RUN mkdir /home/admin/app
WORKDIR /home/admin

COPY requirements.txt ./
RUN pip install -r ./requirements.txt
COPY ./run.sh ./

ENTRYPOINT [ "/bin/bash", "./run.sh" ]
