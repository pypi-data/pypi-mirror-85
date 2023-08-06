# -*- coding: utf-8 -*-
import argparse
import os
import signal
import sys

import gevent
from gevent.pywsgi import WSGIServer

from fserver import conf
from fserver import path_util
from fserver import util
from fserver.fserver_app import app as application


def args():
    parser = argparse.ArgumentParser('fserver')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='run with debug mode')
    parser.add_argument('-u', '--upload', action='store_true',
                        help='run with upload file function')
    parser.add_argument('-o', '--override', action='store_true',
                        help='override mode for upload file')
    parser.add_argument('-i', '--ip', default=conf.BIND_IP,
                        help='ip address for listening, default {}'.format(conf.BIND_IP))
    parser.add_argument('-p', '--port', type=int, default=conf.BIND_PORT,
                        help='port for listening, default 2000')
    parser.add_argument('-r', '--root', metavar='PATH', default=conf.ROOT,
                        help='root path for server, default current path')
    parser.add_argument('-a', '--allow', nargs='+', metavar='PATH', default=tuple(),
                        help='run with allow_list. Only [PATH ...] will be accessed')
    parser.add_argument('-b', '--block', nargs='+', metavar='PATH', default=tuple(),
                        help='run with block_list. [PATH ...] will not be accessed')
    parser.add_argument('-s', '--string', default=conf.STRING,
                        help='share string only')
    parser.add_argument('-v', '--version', action='store_true',
                        help='print version info')

    return parser


def run_fserver():
    _conf = args().parse_args()
    _conf.root = path_util.normalize_path(_conf.root)

    if _conf.version:
        msg = 'fserver {} build at {}\nPython {}'.format(conf.VERSION, conf.BUILD_TIME, sys.version)
        print(msg)
        sys.exit()

    conf.DEBUG = _conf.debug
    conf.UPLOAD = _conf.upload
    conf.UPLOAD_OVERRIDE_MODE = _conf.override
    conf.BIND_IP = _conf.ip
    conf.BIND_PORT = _conf.port
    conf.STRING = _conf.string
    conf.ROOT = path_util.normalize_path(os.path.abspath(_conf.root))

    _root_dir = os.path.abspath(conf.ROOT) + os.sep
    for _afn in _conf.allow:
        afn = path_util.normalize_path(_afn)
        fns = path_util.ls_reg(afn)
        for _fn in fns:
            fn = os.path.abspath(_fn)
            if fn.startswith(_root_dir):
                _ = path_util.normalize_path(fn[len(_root_dir):])
                conf.ALLOW_LIST.add(_)
                for __ in path_util.parents_path(_):
                    conf.ALLOW_LIST_PARENTS.add(path_util.normalize_path(__))

    for _bfn in _conf.block:
        bfn = path_util.normalize_path(_bfn)
        fns = path_util.ls_reg(bfn)
        for _fn in fns:
            fn = os.path.abspath(_fn)
            if fn.startswith(_root_dir):
                conf.BLOCK_LIST.add(path_util.normalize_path(fn[len(_root_dir):]))
    _conf.allow = conf.ALLOW_LIST
    _conf.block = conf.BLOCK_LIST
    u = _conf.allow and _conf.block
    if len(u) > 0:
        print('a path should not be in allow list and block list at the same time: \n{}'.format(list(u)))
        exit()

    if conf.STRING is not None:
        conf.ALLOW_LIST.clear()
        conf.ALLOW_LIST.add('')
        conf.ALLOW_LIST_PARENTS.clear()

    try:
        os.chdir(conf.ROOT)
    except:
        print('invalid root: {}'.format(conf.ROOT))
        exit(-1)

    if conf.DEBUG:
        print(conf.debug_msg(_conf))

    print('fserver is available at following address:')
    if conf.BIND_IP == '0.0.0.0':
        ips = util.get_ip_v4()
        for _ip in ips:
            print('  http://%s:%s' % (_ip, conf.BIND_PORT))
    else:
        print('  http://%s:%s' % (conf.BIND_IP, conf.BIND_PORT))

    gevent.signal_handler(signal.SIGINT, _quit)
    gevent.signal_handler(signal.SIGTERM, _quit)
    http_server = WSGIServer((conf.BIND_IP, int(conf.BIND_PORT)), application)
    http_server.serve_forever()


def _quit():
    print('Bye')
    sys.exit(0)


if __name__ == '__main__':
    run_fserver()
