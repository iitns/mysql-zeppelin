FROM --platform=linux/arm64 python:3.12.4

USER root

RUN apt update && apt upgrade
RUN apt install -y default-mysql-client 

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ENV MYSQL_HOST=mysql-server \
    MYSQL_PORT=3306 \
    MYSQL_USER=iitns  \
    MYSQL_PASSWORD=default-password \
    MYSQL_DATABASE=iitns

COPY init.sh /app/init.sh
RUN chmod +x /app/init.sh

COPY init-schema.sql /app/init-schema.sql
