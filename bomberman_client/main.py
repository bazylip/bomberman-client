from bomberman_client.player.player import Player

player = Player()
print("Waiting for opponent to join...")
player.update_player_info()
print("Ready!")
print(player.get_player_info())