import time
import keyboard

from threading import Thread


class KeyHandler(Thread):
    def __init__(self, key_queue, communication_queue):
        super().__init__()
        self.key_queue = key_queue
        self.communication_queue = communication_queue

    def check_key_pressed(self):
        keys = ["w", "s", "a", "d", "q", "up", "down", "right", "left", "b"]
        for key in keys:
            if keyboard.is_pressed(key):
                return key
        return None

    def run(self):
        key_down = False
        while True:
            if not self.communication_queue.empty():
                message = self.communication_queue.get()
                if message == "end":
                    break
            key = self.check_key_pressed()
            if key is not None:
                if not key_down:
                    key_down = True
                    self.key_queue.put(key)
            else:
                key_down = False
                pass
