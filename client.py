import socket
import sys

def create_pack(arg):
    s=""
    for i in arg:
        s+=str(i)+","
    s=s.rstrip(",")
    return bytes(s,"utf-8")

HOST, PORT = "diamant-s.ru", 9999
data = bytes(",".join(sys.argv[1:]),'utf-8')
#args=('session',1,1)
#data=create_pack(args)
# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
if sys.argv[1]=='session':
    sock.sendto(data, (HOST, PORT))
    received = str(sock.recv(1024), "utf-8")
    data=bytes('state',"utf-8")
    sock.sendto(data, (HOST, PORT))

print("Sent:     {}".format(data))
print("Received: {}".format(received))
