import socket, select
import random

#FIXME(bat):https://linux.die.net/man/4/epoll
#参考资料:https://yq.aliyun.com/articles/41979

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'

def init_sock():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('localhost', 6666))
    serversocket.listen(1)
    serversocket.setblocking(0)

#初始化socket
init_sock()

#调用系统的epoll_create函数，完成内核事件表注册，用来登记用户感兴趣的socket描述符
epoll = select.epoll()

#调用内核的epoll_ctl函数，向内核事件表里添加listen读事件
epoll.register(serversocket.fileno(), select.EPOLLIN)

try:
   connections = {}; requests = {}; responses = {}
   while True:
      events = epoll.poll(1)
      for fileno, event in events:
         if fileno == serversocket.fileno():
             #如果是listen监听到新链接而就绪，则调用accept函数接收客户端连接
            connection, address = serversocket.accept()
            connection.setblocking(0)
            #把新的连接socket描述符添加到事件表，当下一次epoll_wait返回时就可以帮用户代理socket了
            epoll.register(connection.fileno(), select.EPOLLIN)
            connections[connection.fileno()] = connection
            requests[connection.fileno()] = b''
            responses[connection.fileno()] = "Hello, i am epoll, and the random is "+ str(random.randint(1,100))
         elif event & select.EPOLLIN:
             #读就绪，此时说明是已经建立连接的客户端发来数据了，取其socket描述符，进行recv即可
            requests[fileno] += connections[fileno].recv(1024)
            if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
               epoll.modify(fileno, select.EPOLLOUT)
               connections[fileno].setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 1)
               print('-'*40 + '\n' + requests[fileno].decode()[:-2])
         elif event & select.EPOLLHUP:
            epoll.unregister(fileno)
            connections[fileno].close()
            del connections[fileno]
finally:
   #如果出现异常，在结束进程之前，需要释放资源。故，这里要移除listen描述符，关闭epoll内核事件表，关闭socket等
   epoll.unregister(serversocket.fileno())
   epoll.close()
   serversocket.close()
