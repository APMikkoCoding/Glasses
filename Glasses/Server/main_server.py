import socket

class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.PORT = 5050
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def create_server(self):
        self.server.bind((self.ip, self.PORT))
        print(f'Server IP: {self.ip}')
        self.server.listen(5)

    def listen_for_client(self):
        self.client, self.addr = self.server.accept()
    
    def send_data(self, data):
        self.client.send(data)

    def recv_data(self):
        return self.client.recv(1024)
    
    def close_server(self):
        self.server.close()

server = Server()
server.create_server()
server.listen_for_client()
server.send_data('DISPLAY: Hello'.encode('utf-8'))
server.close_server()