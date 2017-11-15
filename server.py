import socketserver

class session:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def move(self, x1, y1, x2, y2):
        self.p1.x1 += x1
        self.p1.y1 += y1
        self.p2.x2 += x2
        self.p2.y2 += y2

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()