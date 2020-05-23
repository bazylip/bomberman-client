import json
import time
from queue import Queue
from bomberman_client.player.communicator import Communicator


class Player:
    def __init__(self, port=15000):
        self.sending_queue = Queue()
        self.listening_queue = Queue()
        self.communicator = Communicator(player_sending_queue=self.sending_queue,
                                         player_listening_queue=self.listening_queue,
                                         port=port)
        self.communicator.start()
        self.hp = None
        self.location = self.Coordinates(None, None)
        self.id = None

    def update_player_info(self):
        json_info = self.get_player_info_from_server()
        dict_info = json.loads(json_info)
        self.id = dict_info["id"]
        self.location.x = dict_info["x"]
        self.location.y = dict_info["y"]
        self.hp = dict_info["hp"]

    def get_player_info_from_server(self):
        if self.listening_queue:
            message = self.listening_queue.get()
            print(f"New player info: {message}")
        return message

    def get_player_info(self):
        dict_info = {"id": self.id,
                     "x": self.location.x,
                     "y": self.location.y,
                     "hp": self.hp}
        return dict_info

    class Coordinates:
        def __init__(self, x, y):
            self.x = x
            self.y = y

if __name__ == "__main__":
    player1 = Player()
    player2 = Player()
    player1.update_player_info()
    print(player1.get_player_info())