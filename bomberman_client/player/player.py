import json
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

    def update_player_info(self, json_info, init=False):
        dict_info = json.loads(json_info)
        if not init:
            player_name = "player" + str(self.id)
            dict_info = dict_info[player_name]
        self.id = dict_info["id"]
        self.location.x = dict_info["x"]
        self.location.y = dict_info["y"]
        self.hp = dict_info["hp"]

    def get_initial_info(self):
        message = self.listening_queue.get()
        self.update_player_info(message, init=True)

    def get_info_from_server(self):
        message = None
        if not self.listening_queue.empty():
            message = self.listening_queue.get()
        return message

    def send_action_to_server(self, action):
        message_dict = {"id": self.id, "action": action}
        self.sending_queue.put(json.dumps(message_dict))

    def get_player_info(self):
        dict_info = {"id": self.id,
                     "x": self.location.x,
                     "y": self.location.y,
                     "hp": self.hp}
        return json.dumps(dict_info)

    def get_player_location(self):
        return self.location.x, self.location.y

    class Coordinates:
        def __init__(self, x, y):
            self.x = x
            self.y = y

if __name__ == "__main__":
    player = Player()
    print(player.get_player_info())