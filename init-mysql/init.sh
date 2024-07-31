#!/bin/bash

env

mysql -h${MYSQL_HOST} \
    -P${MYSQL_PORT} \
    -u${MYSQL_USER} \
    -p${MYSQL_PASSWORD} \
    ${MYSQL_DATABASE} \
    < /app/init-schema.sql

