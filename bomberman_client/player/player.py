import socket
from queue import Queue
from threading import Thread

from bomberman_client.player.sender import Sender
from bomberman_client.player.listener import Listener


class Player(Thread):
    def __init__(self,
                address=socket.gethostbyname(socket.gethostname()),
                port=15000):
        super().__init__()
        self.address = address
        self.port = port

    def create_player(self):
        sending_socket, listening_socket, server = self._connect_to_server()
        self.sending_queue = Queue()
        self.listening_queue = Queue()
        self.sender = Sender(self.sending_queue,
                             sending_socket)
        self.listener = Listener(self.listening_queue,
                                 listening_socket,
                                 server)

    def start_communication_with_server(self):
        self.listener.start()
        self.sender.start()

    def close_communication_with_server(self):
        player1.sending_queue.put("end client")
        player2.sending_queue.put("end client")

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
        listening_socket, client = create_listening_socket(socket.gethostbyname(socket.gethostname()),
                                                           self.port)

        return sending_socket, listening_socket, client

    def run(self):
        self.start_communication_with_server()
        self.listener.join()
        self.close_communication_with_server()

if __name__ == "__main__":
    player1 = Player(port=15000)
    player1.create_player()
    player2 = Player(port=15001)
    player2.create_player()
    player1.start()
    player2.start()
