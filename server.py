import socket
import threading
import random
import socketserver
class player:
    def __init__(self,ip="0",x=0,y=0):
        self.ip=ip
        self.x=x
        self.y=y
        self.state='first turn'
        
class session:
    def __init__(self, p1=player(), p2=player()):
        self.p1 = p1
        self.p2 = p2
        self.state="wait"
    def move(self, x1, y1, x2, y2):
        self.p1.x += x1
        self.p1.y += y1
        self.p2.x += x2
        self.p2.y += y2

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    sessions=[session()]
    
    def cordinate_oponent(self):
        for i in self.sessions:
            if i.p1.ip == self.client_address[0]:
                return "cord op,"+str(i.p2.x)+str(i.p2.y)
            elif i.p2.ip == self.client_address[0]:
                return "cord op,"+str(i.p1.x)+str(i.p1.y)


    def move(self,x,y):
        res='wait'
        for i in self.sessions:
            #if (i.p1.state == 'first turn' and i.p1.ip == self.client_address[0]) or (i.p2.state == 'first turn' and i.p2.ip == self.client_address[0]):
            #    if random.random()>=0 and random.random()<0.5:
            #        i.p1.state='turn'
            #        i.p2.state='wait'
            #    else:
            #        i.p2.state='turn'
            #        i.p1.state='wait'
            #    return 

            if i.p1.state == 'turn' and i.p1.ip == self.client_address[0]:
                i.p1.x+=x
                i.p1.y+=y
                i.p1.state='wait'
                i.p2.state='turn'
                res='cordinate,'+str(i.p1.x)+','+str(i.p1.y)+','+i.p1.state
            elif i.p2.state == 'turn' and i.p2.ip == self.client_address[0]:
                i.p2.x+=x
                i.p2.y+=y
                i.p2.state='wait'
                i.p2.state='turn'
                res='cordinate,'+str(i.p2.x)+','+str(i.p2.y)+','+i.p2.state
        return res

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
                i.state="game"
                break
        if k==0:
            self.sessions.append(session(player(self.client_address[0],x,y),player()))
            res='wait opponent'
        return  res+' '+str(self.sessions.__len__())+' '+str(self.sessions[self.sessions.__len__()-1].p1.ip)+' '+str(self.sessions[self.sessions.__len__()-1].p2.ip)

    def state(self):
        for i in self.sessions:
            res="error"
            if (i.p1.state == 'first turn' and i.p1.ip == self.client_address[0]) or (i.p2.state == 'first turn' and i.p2.ip == self.client_address[0]):
                if random.random()>=0 and random.random()<0.5:
                    i.p1.state='turn'
                    i.p2.state='wait'
                else:
                    i.p2.state='turn'
                    i.p1.state='wait'

            if i.p1.ip == self.client_address[0]:
                res=i.p1.state
                break
            elif i.p2.ip == self.client_address[0]:
                res=i.p2.state
                break
        return "state,"+res

    def handle(self):
        
        data = self.request[0].split(b',')
        res="nothing change"
        print(data[0].decode('utf-8'))

        if str(data[0].decode('utf-8'))=='session':
            res=self.session_act(int(data[1].decode('utf-8')),int(data[2].decode('utf-8')))
        elif str(data[0].decode('utf-8'))=='move':
            res=self.move(int(data[1].decode('utf-8')),int(data[2].decode('utf-8')))
        elif str(data[0].decode('utf-8'))=='state':
            res=self.state()
        elif str(data[0].decode('utf-8'))=='op':
            res=self.cordinate_oponent()
        
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        
        socket.sendto(bytes(res,"utf-8"), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "diamant-s.ru", 9999
    server = ThreadedUDPServer((HOST, PORT), MyUDPHandler)
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    server.serve_forever()