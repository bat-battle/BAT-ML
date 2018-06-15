#!/usr/bin/env python
# -*- coding: utf-8 -*-
# read from stdin and get response from server write to stdout
import sys
import socket

def socket_cli():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8888))

    while True:
#        data = raw_input("client say: ")
        data = sys.stdin.readline()
        if data.strip() == 'over':
            break
        s.send(data)
        rs = s.recv(1024)
        print "server say: ", rs
    s.send('exit')
    s.close()
    return

socket_cli()

