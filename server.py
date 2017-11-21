import socket
import threading
import socketserver
class player:
    def __init__(self,ip="0",x=0,y=0):
        self.ip=ip
        self.x=x
        self.y=y
        
class session:
    def __init__(self, p1=player(), p2=player()):
        self.p1 = p1
        self.p2 = p2
    def move(self, x1, y1, x2, y2):
        self.p1.x += x1
        self.p1.y += y1
        self.p2.x += x2
        self.p2.y += y2

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    sessions=[session()]
    
    def session_act(self,x,y):
        k=0
        for i in self.sessions:
            if i.p1.ip=='0':
                i.p1.ip=self.client_address[0]
                i.p1.x=x
                i.p1.y=y
                k=1
                res='wait opponent'
                break   
            elif i.p2.ip=='0':
                i.p2.ip=self.client_address[0]
                i.p2.x=x
                i.p2.y=y
                k=1
                res='finded opponent'
                break
        if k==0:
            self.sessions.append(session(player(self.client_address[0],x,y),player()))
            res='wait opponent'
        return  res+' '+str(self.sessions.__len__())+' '+str(self.sessions[self.sessions.__len__()-1].p1.ip)+' '+str(self.sessions[self.sessions.__len__()-1].p2.ip)

    def handle(self):
        
        data = self.request[0].split(b',')
        res="nothing change"
        print(data[0].decode('utf-8'))
        if str(data[0].decode('utf-8'))=='session':
            res=self.session_act(int(data[1].decode('utf-8')),int(data[2].decode('utf-8')))
           
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        
        socket.sendto(bytes(res,"utf-8"), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()