from queue import Queue

from bomberman_client.game.key_handler import KeyHandler


class EventHandler():
    def __init__(self):
        self.key_queue = Queue()
        self.communication_queue = Queue()
        self.key_handler = KeyHandler(self.key_queue, self.communication_queue)
        self.key_handler.start()

    def get_user_action(self):
        action = None
        if not self.key_queue.empty():
            action = self.key_queue.get()
            if action not in self.key_set:
                action = None
            if action in ["w", "s", "a", "d", "q"]:
                action = self.key_dict.get(action)
        return action

    def set_keys(self, id):
        if id == 1:
            self.key_set = ["up", "down", "right", "left", "b"]
        elif id == 2:
            self.key_set = ["w", "s", "a", "d", "q"]
            self.key_dict = {"w": "up", "s": "down", "a": "left", "d": "right", "q": "b"}

    def stop_event_handler(self):
        self.communication_queue.put("end")