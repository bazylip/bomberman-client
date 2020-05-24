from bomberman_client.game.event_handler import EventHandler

class GameMechanics(EventHandler):
    def __init__(self):
        super().__init__()

    def process_user_action(self, player, action):
        if action == "up":
            player.location.y += 1
        elif action == "down":
            player.location.y -= 1
        elif action == "right":
            player.location.x += 1
        elif action == "left":
            player.location.x -= 1
        return player