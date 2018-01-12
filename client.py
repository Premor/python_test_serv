import socket
import sys
import tkinter



class client:
    class cell:
        def __init__(self,state='open')
            self.state=state
    maps=[]
    adj=[]
    HOST = "diamant-s.ru"  
    PORT = 9999
    state=""
    def create_pack(self,arg):
        s=""
        for i in arg:
            s+=str(i)+";"
        s=s.rstrip(";")
        return bytes(s,"utf-8")

    def map_generate(self):
        for i in range(0,8):
            self.maps.append(list())
            for j in range(0,8):
                self.maps[i].append(self.cell())
        for i in range(0,8):
            self.adj.append(list())
            for j in range(0,8):
                self.adj[i].append(list())
                if i+1 in range(0,8):
                    self.adj[i][j].append([i+1,j])
                    if i%2==0:
                        if j-1 in range(0,8):
                            self.adj[i][j].append([i+1,j-1])
                    else:
                        if j+1 in range(0,8):
                            self.adj[i][j].append([i+1,j+1])
                if i-1 in range(0,8):
                    self.adj[i][j].append([i-1,j])
                    if i%2==0:
                        if j-1 in range(0,8):
                            self.adj[i][j].append([i-1,j-1])
                    else:
                        if j+1 in range(0,8):
                            self.adj[i][j].append([i-1,j+1])
                if j+1 in range(0,8):
                    self.adj[i][j].append([i,j+1])
                if j-1 in range(0,8):
                    self.adj[i][j].append([i,j-1])

                if i-1 in range(0,8) and i%2==0:
                    self.adj[i][j].append()

    def session_act(self,event):
                
        #data = bytes(";".join(sys.argv[1:]),'utf-8')
        args=('session',"slave:333,archer:50")
        data=self.create_pack(args)
        #data=bytes()
    # SOCK_DGRAM is the socket type to use for UDP sockets
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # As you can see, there is no connect() call; UDP has no connections.
    # Instead, data is directly sent to the recipient via sendto().
        sock.sendto(data, (self.HOST, self.PORT))
        received = str(sock.recv(1024), "utf-8")
        self.state['text']=received
    def __init__(self):
        self.map_generate()
        root = tkinter.Tk()
        image = tkinter.PhotoImage(file='./setka.png')
        btn = tkinter.Button(root,text="Click me",width=30,height=5)
        lab= tkinter.Label(root,text="state")
        lab2= tkinter.Label(root,image=image)
        lab2.pack()
        self.state=lab
        lab.pack()
        btn.bind("<Button-1>",self.session_act)
        btn.pack()
        root.mainloop()


a=client()
