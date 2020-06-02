from pynput.keyboard import Key, KeyCode, Listener
from threading import Thread


class KeyHandler(Thread):
    def __init__(self, key_queue, communication_queue):
        super().__init__()
        self.key_queue = key_queue
        self.communication_queue = communication_queue

    def on_press(self, key):
        keys_dict = {KeyCode.from_char('w'): "w", KeyCode.from_char('s'): "s",
                     KeyCode.from_char('a'): "d", KeyCode.from_char('d'): "a",
                     KeyCode.from_char('q'): "q", Key.up: "up",
                     Key.down: "down", Key.right: "left",
                     Key.left: "right", KeyCode.from_char('b'): "b"}
        if key in list(keys_dict.keys()):
            self.key_queue.put(keys_dict.get(key))

    def run(self):
        listener = Listener(on_press=self.on_press).start()
        while True:
            if not self.communication_queue.empty():
                message = self.communication_queue.get()
                if message == "end":
                    listener.stop()
                    break
