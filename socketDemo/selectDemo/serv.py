#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import select

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(False)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 8888))
#import ipdb; ipdb.set_trace() ### XXX BREAKPOINT

s.listen(10)

#rlist用来保存需要select向内核询问读事件是否就绪（新链接和客户发来数据）
#为了简单起见，这里就不注册写时间给select函数了，而是直接把客户端的数据发回去
rlist = [s]
wlist = []
xlist = []
closed = []
timeout = 2

while True:
    ready_rl, ready_wl, ready_xl = select.select(rlist, wlist, xlist, timeout)
    for sock in ready_rl:
        if sock is s:
            sock, addr = s.accept()
            sock.setblocking(False)
            rlist.append(sock)
        else:
            data = sock.recv(1024)
            if data == '' or data == 'exit':
                closed.append(sock)
            else:
                sock.send(data)
    for sock in ready_xl:
        print '%s:%s error occur' % sock.getpeername()
        closed.append(sock)
    for cs in closed:
        try:
            rlist.remove(cs)
            xlist.remove(cs)
        except ValueError:
            pass

        cs.close()

    closed = []
    if len(rlist) == 0:
        break
