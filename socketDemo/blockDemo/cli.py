#Echo client program
import socket

HOST = 'localhost'    # The remote host
PORT = 8080              # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    say = raw_input("cli say: ")
    s.sendall(say)
    data = s.recv(1024)
    print 'ser say:', repr(data)
    if say.lower() == 'quit':
        break
s.close()
