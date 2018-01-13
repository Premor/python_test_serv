import time
import socket
import threading
import random
import socketserver

class unit:
    def __init__(self,count=1,x=0,y=0,hp=10,damage=5,move=3,range_=1):
        self.initiat=0
        self.count=count
        self.max_hp=hp
        self.current_hp=hp
        self.damage=damage
        self.move=move
        self.range=range_
        self.x=x
        self.y=y
        self.mode='attack'
        self.udalennost=0 #удаленность от центра 
        self.last_cell=[]
        
    
class slave(unit):
    def __init__(self,count=1,x=0,y=0):
        super().__init__(count,x,y,15,3,8,1)
class archer(unit):
    def __init__(self,count=1,x=0,y=0):
        super().__init__(count,x,y,5,7,4,4)


class player:
    def __init__(self,ip="0",x=0,y=0):
        self.ip=ip
        self.x=x
        self.y=y
        self.state='first turn'
        self.units=[]
        self.path=[]
    def apllay_move(self,s):
        i=0
        while i<len(s):
            self.units[i].x= s[i][0]
            self.units[i].y= s[i][1]
            i+=1


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
    
    def coordinate_opponent(self):
        res=''
        for i in self.sessions:
            if i.p1.ip == self.client_address[0]:
                arg=[]
                for j in i.p1.units:
                    arg.append([j.x,j.y])
                return "coord_op;"+list_pack(arg)
            elif i.p2.ip == self.client_address[0]:
                arg=[]
                for j in i.p2.units:
                    arg.append([j.x,j.y])
                return "coord_op;"+list_pack(arg)


    def max_move(self,ses):
        t=[]
        for i in range(0,len(ses.p1.units)):
            t.append(ses.p1.units[i].move)
        for i in range(0,len(ses.p2.units)):
            t.append(ses.p2.units[i].move)
        return max(t)
    def move_phase(self,ses):
        for i in range(0,len(ses.p1.units)):
            ses.p1.units[i].rem_move=ses.p1.units[i].move
            ses.p1.units[i].udalennost=0
            ses.p1.units[i].last_cell=[ses.p1.units[i].x,ses.p1.units[i].y]
        for i in range(0,len(ses.p2.units)):
            ses.p2.units[i].rem_move=ses.p2.units[i].move
            ses.p2.units[i].last_cell=[ses.p2.units[i].x,ses.p2.units[i].y]
            ses.p2.units[i].udalennost=0
        #глобальный цикл по скорости
        for i in range(0,self.max_move(ses)):
            for j in range(0,len(ses.p1.units)):
                if ses.p1.path!=[] and ses.p1.units[j].x!=ses.p1.path[0][0] and ses.p1.units[j].y!=ses.p1.path[0][1] and ses.p1.units[j].rem_move>0:
                    if ses.p1.units[j].udalennost <2:
                        ses.p1.units[j].udalennost+=1
                    else:
                        ses.p1.units[j].x=ses.p1.path[0][0]
                        ses.p1.units[j].y=ses.p1.path[0][1]
                    ses.p1.units[j].rem_move-=1
                elif ses.p1.path!=[] and ses.p1.units[j].x==ses.p1.path[0][0] and ses.p1.units[j].y==ses.p1.path[0][1] and ses.p1.units[j].rem_move>0:
                    if ses.p1.units[j].udalennost >0:
                        ses.p1.units[j].udalennost-=1
                        if ses.p1.units[j].udalennost==0:
                            ses.p1.units[j].last_cell=[ses.p1.units[j].x,ses.p1.units[j].y]
                    else:
                        ses.p1.path.pop(0) #WARNING вроде помню что это дерьмо когда-то не работало, если будут проблемы заменить
                        ses.p1.units[j].udalennost+=1
                    ses.p1.units[j].rem_move-=1

            for j in range(0,len(ses.p2.units)):
                if ses.p2.path!=[] and ses.p2.units[j].x!=ses.p2.path[0][0] and ses.p2.units[j].y!=ses.p2.path[0][1] and ses.p2.units[j].rem_move>0:
                    if ses.p2.units[j].udalennost <2:
                        ses.p2.units[j].udalennost+=1
                    else:
                        ses.p2.units[j].x=ses.p2.path[0][0]
                        ses.p2.units[j].y=ses.p2.path[0][1]
                    ses.p2.units[j].rem_move-=1
                elif ses.p2.path!=[] and ses.p2.units[j].x==ses.p2.path[0][0] and ses.p2.units[j].y==ses.p2.path[0][1] and ses.p2.units[j].rem_move>0:
                    if ses.p2.units[j].udalennost >0:
                        ses.p2.units[j].udalennost-=1
                        if ses.p2.units[j].udalennost==0:
                            ses.p2.units[j].last_cell=[ses.p2.units[j].x,ses.p2.units[j].y]
                    else:
                        ses.p2.path.pop(0) #WARNING вроде помню что это дерьмо когда-то не работало, если будут проблемы заменить
                        ses.p2.units[j].udalennost+=1
                    ses.p2.units[j].rem_move-=1
            #нужны проверки на встречу
            for j in ses.p1.units:
                for l in ses.p2.units:
                    if j.x == l.x and j.y == l.y:
                        total_hp_1=j.max_hp*j.count
                        total_hp_2=l.max_hp*l.count
                        total_dmg_1=j.damage*j.count
                        total_dmg_2=l.damage*l.count
                        total_hp_1-=total_dmg_2
                        total_hp_2-=total_dmg_1
                        if total_hp_1<=0:
                            j.state='dead'
                        else:
                            j.count=total_hp_1//j.max_hp
                            j.current_hp=total_hp_1%j.max_hp
                            j.x=j.last_cell[0]
                            j.y=j.last_cell[1]
                            ses.p1.path=[]
                        if total_hp_2<=0:
                            l.state='dead'
                        else:
                            l.count=total_hp_2//l.max_hp
                            l.current_hp=total_hp_2%l.max_hp
                            l.x=l.last_cell[0]
                            l.y=l.last_cell[1]
                            ses.p2.path=[]
                        


    def move(self,coord):
        res='wait'
        for i in self.sessions:
            if i.p1.state == 'turn' and i.p1.ip == self.client_address[0]:
                #p1.apllay_move(coord)
                p1.path=coord
                i.p1.state='wait'
                res='state,'+i.p1.state
            elif i.p2.state == 'turn' and i.p2.ip == self.client_address[0]:
                #p1.apllay_move(coord)
                p1.path=coord
                i.p2.state='wait'
                res='state,'+i.p2.state
            if i.p1.state == 'wait' and i.p2.state == 'wait': 
                self.move_phase(i)
                i.p1.state = 'turn'
                i.p2.state = 'turn'
        return res

    def session_act(self,units):
        k=0
        for i in self.sessions:
            if i.p1.ip=='0':
                i.p1.ip=self.client_address[0]
                i.p1.x=0
                i.p1.y=0
                for j in units:
                    i.p1.units.append(eval("{0}({1})".format(j[0],j[1])))
                k=1
                res='wait opponent'
                break   
            elif i.p2.ip=='0':
                i.p2.ip=self.client_address[0]
                i.p2.x=10
                i.p2.y=10
                k=1
                for j in units:
                    i.p2.units.append(eval("{0}({1})".format(j[0],j[1])))
                res='finded opponent'
                i.state="game"
                break
        if k==0:
            self.sessions.append(session(player(),player()))
            i=self.sessions[self.sessions.__len__()-1]
            i.p1.ip=self.client_address[0]
            i.p1.x=0
            i.p1.y=0
            for j in units:
                    i.p1.units.append(eval("{0}({1})".format(j[0],j[1])))
            k=1
            res='wait opponent'
        return  res+' '+str(self.sessions.__len__())+' '+str(self.sessions[self.sessions.__len__()-1].p1.ip)+' '+str(self.sessions[self.sessions.__len__()-1].p2.ip)

    def state(self):
        for i in self.sessions:
            res="error"
            if (i.p1.state == 'first turn' and i.p1.ip == self.client_address[0]) or (i.p2.state == 'first turn' and i.p2.ip == self.client_address[0]):
                #if random.random()>=0 and random.random()<0.5:
                #    i.p1.state='turn'
                #    i.p2.state='wait'
                #else:
                #    i.p2.state='turn'
                #    i.p1.state='wait'
                i.p1.state='turn'
                i.p2.state='turn'

            if i.p1.ip == self.client_address[0]:
                res=i.p1.state
                break
            elif i.p2.ip == self.client_address[0]:
                res=i.p2.state
                break
        return "state,"+res

    def handle(self):
        data = self.request[0].split(b';')
        res="nothing change"
        print(data[0].decode('utf-8'))

        if str(data[0].decode('utf-8'))=='session':
            res=self.session_act(parse_list(data[1].decode('utf-8')))
        elif str(data[0].decode('utf-8'))=='move':
            format_data=[]
            for i in range(1,len(data)):
                format_data.append(parse_list(data[i].decode('utf-8')))
            res=self.move(format_data)
        elif str(data[0].decode('utf-8'))=='state':
            res=self.state()
        elif str(data[0].decode('utf-8'))=='op':
            res=self.coordinate_opponent()
        
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        
        socket.sendto(bytes(res,"utf-8"), self.client_address)


def create_pack(arg):
    s=""
    for i in arg:
        s+=str(i)+";"
    s=s.rstrip(";")
    return s

def list_pack(l):
    res=''
    for i in l:
        res+=i[0]+':'+i[1]+','
    res=res.rstrip(",")
    return res

def parse_list(arg):
    args=arg.split(',')
    res=[]
    for i in args:
        buf=i.split(':')
        buf2=[]
        for j in buf:
            buf2.append(j)
        res.append(buf2)
    return res

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
