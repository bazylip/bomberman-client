import socket
from queue import Queue
from sender import Sender
from listener import Listener


class Player:
    def __init__(self, address=socket.gethostbyname(socket.gethostname()), port=15000):
        self.address = address
        self.port = port

    def create_player(self):
        sending_socket, listening_socket, server = self._connect_to_server()
        self.sending_queue = Queue()
        self.listening_queue = Queue()
        self.sender = Sender(self.sending_queue, sending_socket)
        self.listener = Listener(self.listening_queue, listening_socket, server)

    def _connect_to_server(self):
        def create_listening_socket(address, port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((address, port))
            s.listen()
            server, addr = s.accept()
            print(f"New connection from server: {addr}")
            return s, server

        def create_sending_socket(address, port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.address, self.port))
            self.client_socket = s
            print(f"Connected to {address} on {port}")
            return s

        sending_socket = create_sending_socket(self.address, self.port)
        listening_socket, client = create_listening_socket(socket.gethostbyname(socket.gethostname()), self.port)

        return sending_socket, listening_socket, client

if __name__ == "__main__":
    player1 = Player(port=15000)
    player1.create_player()
    player2 = Player(port=15001)
    player2.create_player()