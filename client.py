import socket
import sys
import tkinter
class client:
    HOST = "diamant-s.ru"  
    PORT = 9999
    state=""
    def create_pack(self,arg):
        s=""
        for i in arg:
            s+=str(i)+";"
        s=s.rstrip(";")
        return bytes(s,"utf-8")

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
        root = tkinter.Tk()
        btn = tkinter.Button(root,text="Click me",width=30,height=5)
        lab= tkinter.Label(root,text="state")
        self.state=lab
        lab.pack()
        btn.bind("<Button-1>",self.session_act)
        btn.pack()
        root.mainloop()

a=client()