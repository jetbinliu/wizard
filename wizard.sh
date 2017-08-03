#!/bin/bash

GUNICORN_BIN='/root/.virtualenvs/py3.6/bin/gunicorn'
CONFIG_FILE='./conf/gunicorn_config.py'
APPLICATION_WSGI='wizard.wsgi'
OP=${1:-*}

function stop() {
    /bin/ps -ef | /bin/grep gunicorn | /bin/awk '{print $2}' | /usr/bin/xargs /bin/kill -15 &>/dev/null
}

function start() {
    ${GUNICORN_BIN} --config=${CONFIG_FILE} ${APPLICATION_WSGI}
}

function reload() {
    masterpid=`/bin/ps -ef | /bin/grep -E "^root.*gunicorn" | /bin/grep -v "grep" | /bin/awk '{print $2}'`
    /bin/kill -1 ${masterpid}
}

function restart() {
    stop
    sleep 3
    start
}

function status() {
    /bin/ps -ef | /bin/grep gunicorn | /bin/grep -v "grep"    
}

function increase() {
    masterpid=`/bin/ps -ef | /bin/grep -E "^root.*gunicorn" | /bin/grep -v "grep" | /bin/awk '{print $2}'`
    /bin/kill -21 ${masterpid}
}

function decrease() {
    masterpid=`/bin/ps -ef | /bin/grep -E "^root.*gunicorn" | /bin/grep -v "grep" | /bin/awk '{print $2}'`
    /bin/kill -22 ${masterpid}
}

case "$OP" in

    'start')
        start
        ;;

    'stop')
        stop
        ;;

    'restart')
        restart
        ;;

    'reload')
        reload
        ;;
    
    'status')
        status
        ;;

    'increase')
        increase
        ;;

    'decrease')
        decrease
        ;;
        
    *)
        echo "Usage: $0 { start | stop | restart | reload | status | increase | decrease }"
        exit 1
        ;;
esac

exit 0

