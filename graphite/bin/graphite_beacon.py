#!/usr/bin/env python
# -×- coding:utf-8 -×-
# Created by lilx on 14-12-30.
__author__ = 'lilx'
import sys
import os
import signal
import logging
from logging.handlers import RotatingFileHandler


cwd = os.path.abspath(os.path.dirname(__file__))
home = os.path.dirname(cwd)
cfg_file = os.path.join(home, 'conf', 'beacon.json')
pid_file = os.path.join(home, 'storage', 'pid', 'beacon.pid')
log_dir = os.path.join(home, 'storage', 'log', 'beacon')
print home, cfg_file, pid_file


MAX_BYTES = 100 * 1024 * 1024
BACKUP_COUNT = 3


def set_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_file_path = os.path.join(log_dir, '%s.log' % name)
    filehandler = RotatingFileHandler(log_file_path, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    logger.setLevel(level)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)


def become_daemon():
    # become daemon
    try:
        if os.fork() > 0:
            os._exit(0)
    except Exception, e:
        print e.message
        os._exit(1)

    os.setsid()
    os.umask(022)

    try:
        pid = os.fork()
        if pid > 0:
            os.system("echo '%s' > %s" % (pid, pid_file))
            print 'graphite beacon daemon pid %s' % pid
            os._exit(0)
    except Exception, e:
        print e.message
        os._exit(1)


def start():
    # become daemon
    # become_daemon()

    # set logger
    set_logger('graphite_beacon')

    beacon_dir = os.path.join(home, 'lib')
    print beacon_dir
    sys.path.append(beacon_dir)
    from beacon.core import Reactor
    options = {
        'config': cfg_file,
        'pidfile': pid_file
    }
    r = Reactor(**options)
    signal.signal(signal.SIGTERM, r.stop)
    signal.signal(signal.SIGINT, r.stop)
    signal.signal(signal.SIGHUP, r.reinit)

    r.start()


def stop():
    with open(pid_file, 'rb') as f:
        pid = f.read()
    try:
        pid = int(pid)
    except:
        pid = 0
    if pid:
        os.system('kill %s' % pid)


def shell():
    script, command = sys.argv[:2]
    script_name = script[:-3]
    command = command.lower()
    if 'start' == command:
        start()
    elif 'stop' == command:
        stop()
    else:
        print 'command %s not found!' % command


if __name__ == '__main__':
    shell()