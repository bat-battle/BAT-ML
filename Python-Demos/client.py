import socket
import sys

port=51423
host="localhost"

data=b"x"*10485760
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((host,port))

byteswritten=0
while byteswritten<len(data):
    startpos = byteswritten
    endpos = min(byteswritten+1024,len(data))
    byteswritten+=sock.send(data[startpos:endpos])
    sys.stdout.write("wrote %d bytes\r"% byteswritten)
    sys.stdout.flush()

sock.shutdown(1)

print("All data sent.")
while True:
    buf = sock.recv(1024).decode()
    if not len(buf):
        break
    sys.stdout.write(buf)
