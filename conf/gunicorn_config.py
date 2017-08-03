# -*- coding: UTF-8 -*-

import os
import sys
import multiprocessing
import logging
import logging.handlers
from logging.handlers import WatchedFileHandler

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
proc_name = "gunicorn.proc"
threads = 2
backlog = 2048
timeout = 1200
debug = False
daemon = True
reload = True

log_level = 'info' 
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = "/dev/null"
errorlog = "/dev/null"
acclog = logging.getLogger('gunicorn.access')
acclog.addHandler(WatchedFileHandler('/tmp/gunicorn_access.log'))
acclog.propagate = False
errlog = logging.getLogger('gunicorn.error')
errlog.addHandler(WatchedFileHandler('/tmp/gunicorn_error.log'))
errlog.propagate = False

pidfile = "/tmp/gunicorn.pid"
chdir = "/usr/local/wizard"
pythonpath = "/root/.virtualenvs/py3.6"
