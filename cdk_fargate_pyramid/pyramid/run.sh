#!/bin/bash
export SQLALCHEMY_URL=postgresql://postgres:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}
bootstrap
pserve ./config/pyramid/ini/fargate.ini
