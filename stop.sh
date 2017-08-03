#!/bin/bash

#PORT=${1:-8888}
#ps -ef | grep gunicorn | grep ${PORT} | awk '{print $2}' | xargs kill -15 >/dev/null 2>&1
/bin/ps -ef | /bin/grep gunicorn | /bin/awk '{print $2}' | /usr/bin/xargs /bin/kill -15 &>/dev/null
