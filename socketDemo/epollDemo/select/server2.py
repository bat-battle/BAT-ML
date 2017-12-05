import select
import socket
import Queue

#create a socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setblocking(False)
#set option reused
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR  , 1)

server_address= ('localhost', 6666)
server.bind(server_address)

server.listen(10)

#sockets from which we except to read
inputs = [server]

#sockets from which we expect to write
outputs = []

#Outgoing message queues (socket:Queue)
message_queues = {}

#A optional parameter for select is TIMEOUT
timeout = 20

count = 1
while inputs:
    print "waiting for event", count
    readable , writable , exceptional = select.select(inputs, outputs, inputs, timeout)
    print readable, writable, exceptional

    # When timeout reached , select return three empty lists
    if not (readable or writable or exceptional) :
        print "Time out ! "
        break;
    for s in readable :
        if s is server:
            # A "readable" socket is ready to accept a connection
            connection, client_address = s.accept()
            print "    connection from ", client_address
            connection.setblocking(0)
            inputs.append(connection) # atfer append , connection is always in readable list because connection is hold , I think
            message_queues[connection] = Queue.Queue()
        else:
            data = s.recv(1024)
            if data :
                print " received '" , data , "' from ",s.getpeername()
                message_queues[s].put(data)
                # Add output channel for response
                if s not in outputs:
                    outputs.append(s)
            else:
                print 'client is sleeping'
                if s in outputs :
                    outputs.remove(s) # remove it so don't send msg until user accept mgs server sent before and response to server
                #inputs.remove(s)
                #s.close()
                #remove message queue
                #del message_queues[s]
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            print " " , s.getpeername() , 'queue empty'
            outputs.remove(s)
        else:
            print " sending " , next_msg , " to ", s.getpeername()
            s.send(next_msg)

    for s in exceptional:
        print " exception condition on ", s.getpeername()
        #stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        #Remove message queue
        del message_queues[s]
    count +=1
