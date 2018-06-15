#!/usr/bin/env python
# -*- coding: utf-8 -*-
# read from stdin and get response from server write to stdout

import os
import socket
import multiprocessing

dirpath = 'data/'


def work(id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 8888))
        df = open('html')
        tf = open(dirpath + id, 'wb')

        while True:
            line = df.readline()
            if line == '':
                break
            # sock.send('%s: %s' % (id, line))
            sock.send('%s' % line)
            buf = sock.recv(1024)
            tf.write(buf)
        sock.close()
    except IOError as e:
        print 'file error: ', e
    except socket.error as e:
        print 'socket error: ', e


if not os.path.exists(dirpath):
    os.mkdir(dirpath)

for i in range(10):
    p = multiprocessing.Process(target=work, args=('Process%03d' % i,))
    p.run()
