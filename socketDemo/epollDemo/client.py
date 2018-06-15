#coding:utf-8
import socket,select
host = "localhost"
port = 6666
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
s.send("coming from select client\n\n")
response = s.recv(1024)
print response
