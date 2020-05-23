import socket
from queue import Queue
from threading import Thread

from bomberman_client.player.sender import Sender
from bomberman_client.player.listener import Listener


class Communicator(Thread):
    def __init__(self,
                 player_sending_queue,
                 player_listening_queue,
                 port,
                 address=socket.gethostbyname(socket.gethostname())
                 ):
        super().__init__()
        self.player_sending_queue = player_sending_queue
        self.player_listening_queue = player_listening_queue
        self.address = address
        self.port = port
        self.create_sender_and_listener()

    def create_sender_and_listener(self):
        sending_socket, listening_socket, addr = self._connect_to_server()
        self.sending_queue = Queue()
        self.listening_queue = Queue()
        self.sender = Sender(self.sending_queue,
                             sending_socket)
        self.listener = Listener(self.listening_queue,
                                 listening_socket)

    def start_communication_with_server(self):
        self.listener.start()
        self.sender.start()

    def close_communication_with_server(self):
        self.sending_queue.put("end client")

    def get_message_from_server(self):
        received_message = self.listening_queue.get() if self.listening_queue else None
        if received_message is not None:
            self.player_listening_queue.put(received_message)
        return received_message

    def _connect_to_server(self):
        def create_listening_socket(address):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((address, self.port))
            s.listen()
            server, addr = s.accept()
            print(f"New connection from server: {addr}")
            s.close()
            return server, addr

        def create_sending_socket(address):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.address, self.port))
            self.client_socket = s
            print(f"Connected to {address} on {self.port}")
            return s

        sending_socket = create_sending_socket(self.address)
        listening_socket, addr = create_listening_socket(socket.gethostbyname(socket.gethostname()))

        return sending_socket, listening_socket, addr

    def run(self):
        self.start_communication_with_server()
        while True:
            message = self.get_message_from_server()
            if message == "end client":
                break
        self.listener.join()
        self.close_communication_with_server()
