from bomberman_client.game.game_mechanics import GameMechanics
from bomberman_client.game.event_handler import EventHandler
from bomberman_client.gui.game_interface import GameInterface
from bomberman_client.player.player import Player

class Game(GameMechanics, GameInterface):
    def __init__(self):
        super().__init__()

    def start_game(self):
        self.player = Player()
        print("Waiting for opponent to join...")
        self.game_loop()

    def game_loop(self):
        print("Ready")
        self.player.get_initial_info()
        while True:
            info = self.player.get_info_from_server()
            if info is not None:
                if self.server_disconnected(info):
                    self.stop_event_handler()
                    break
                if self.check_win_or_lose(info):
                    self.render_end_screen()
                    break
                self.player.update_player_info(info)
            self.render()
            action = self.get_user_action()
            if action is not None:
                print(f"Action: {action}")
                self.player = self.process_user_action(self.player, action)
                print(f"New player info: {self.player.get_player_info()}")
                self.player.send_action_to_server(action)

    def check_win_or_lose(self, info):
        return False

    def server_disconnected(self, info):
        if info == "end client":
            print("Disconnected by server")
            return True