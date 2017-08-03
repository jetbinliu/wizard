#!/bin/bash

GUNICORN_BIN='/root/.virtualenvs/py3.6/bin/gunicorn'
CONFIG_FILE='./conf/gunicorn_config.py'
APPLICATION_WSGI='wizard.wsgi'

${GUNICORN_BIN} --config=${CONFIG_FILE} ${APPLICATION_WSGI}
