#encoding: utf-8

import socket
import time
HOST = ''
PORT = 8080


def create_sock():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(10)
    return s


def main_loop():
    sock = create_sock()
    while 1:
        #accept函数去listen函数维护的全连接队列里取一条客户端连接，返回一个socket
        #文件描述符，用于和此用户进行数据收发。
        conn, addr = sock.accept()

        #NOTE:设置一个socket描述符为非阻塞，此后拿这个描述符去和
        #系统交互的过程中，所有涉及到阻塞的函数，当需要资源没有准备好，
        #当前进程的CPU不会被剥夺，系统会返回一个错误，告知用户数据没有准备好
        #，接着用户需要间隔性（sleep一定时间）去再去询问系统。
        #虽然CPU没有被剥夺，当前进程可以继续执行代码，但是需要多次从用户态切换
        #到内核态，导致进程上下文切换开销，而此开销对于系统来说，是很重的操作。
#        conn.setblocking(False)
        print 'Connected by', addr
        while True:
            try:
                data = "not data"
                import ipdb; ipdb.set_trace() ### XXX BREAKPOINT
                data = conn.recv(1024)
                print "cli say:", data
            except Exception as ex:
                print "err:", ex.args
                continue
            time.sleep(0.1)
            if not data:
                break
            conn.sendall(data)
        conn.close()

if __name__ == "__main__":
    main_loop()
