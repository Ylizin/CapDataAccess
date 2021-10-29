import os
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

# usage:  gunicorn -c config.py app:app

# debug = True
loglevel = 'debug'
bind = "0.0.0.0:7001"
pidfile = "gunicorn.pid"
accesslog = "access.log"#对应handler 为 gunicorn.access
errorlog = "debug.log" #对应handler 为 gunicorn.error
daemon = False
preload=True
reload = True #reload对应是否在代码修改后重新加载，详见-h

# 启动的进程数
workers = 1#int(multiprocessing.cpu_count()/2)
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'