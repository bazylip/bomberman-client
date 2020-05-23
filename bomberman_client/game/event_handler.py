from queue import Queue

from bomberman_client.game.key_handler import KeyHandler


class EventHandler():
    def __init__(self):
        self.key_queue = Queue()
        self.end_queue = Queue()
        self.key_handler = KeyHandler(self.key_queue, self.end_queue)
        self.key_handler.start()

    def get_user_action(self):
        action = None
        if not self.key_queue.empty():
            action = self.key_queue.get()
        return action

    def stop_event_handler(self):
        self.end_queue.put("end")