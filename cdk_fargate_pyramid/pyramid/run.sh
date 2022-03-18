#!/bin/bash
echo $PATH
bootstrap
pserve ./config/pyramid/ini/fargate.ini
