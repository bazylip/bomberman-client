import json
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


BOARD_DIMENSION_X = 15
BOARD_DIMENSION_Y = 9
RESOLUTION_X = 800
RESOLUTION_Y = 600
GRASS_COLOR = (30,200,0)
BLOCK_COLOR = (91,89,88)
HP_COLOR = (255,0,0)
FIELD_SIZE_X = RESOLUTION_X / BOARD_DIMENSION_X
FIELD_SIZE_Y = RESOLUTION_Y / BOARD_DIMENSION_Y

class GameInterface:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(size=(RESOLUTION_X, RESOLUTION_Y))
        self.player_image = pygame.image.load("gui/images/player2.png").convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (50, 50))
        self.bomb_image = pygame.image.load("gui/images/bomb2.png").convert_alpha()
        self.bomb_image = pygame.transform.scale(self.bomb_image, (60, 60))
        pygame.display.set_caption("Bomberman")

    def render(self, board_state_json, player_id):
        if board_state_json is not None:
            board_state = json.loads(board_state_json)
            self.display.fill(GRASS_COLOR)
            self._render_blocks()
            self._render_players(board_state, player_id)
            self._render_bombs(board_state)
            pygame.display.update()

    def _render_blocks(self):
        for block_x in range(1, 15, 2):
            for block_y in range(1, 9, 2):
                pygame.draw.rect(self.display,
                                 BLOCK_COLOR,
                                 [block_x*FIELD_SIZE_X, block_y*FIELD_SIZE_Y,
                                  FIELD_SIZE_X, FIELD_SIZE_Y]
                                 )

    def _render_players(self, board_state, player_id):
        def render_hp(player):
            initial_x = player.get("x")
            y = player.get("y")
            for block_num in range(int(player.get("hp") / 25)):
                pygame.draw.rect(self.display,
                                 HP_COLOR,
                                 [RESOLUTION_X - player.get("x")*FIELD_SIZE_X + block_num * FIELD_SIZE_X/4,
                                  RESOLUTION_Y - player.get("y")*FIELD_SIZE_Y + 55,
                                  10,
                                  10]
                                 )


        players = [board_state.get("player1"), board_state.get("player2")]
        for player in players:

            self.display.blit(self.player_image, (RESOLUTION_X - player.get("x")*FIELD_SIZE_X,
                                                  RESOLUTION_Y - player.get("y")*FIELD_SIZE_Y))
            render_hp(player)

    def _render_bombs(self, board_state):
        bombs = board_state.get("bombs")
        if bombs is not None:
            for bomb in bombs:
                self.display.blit(self.bomb_image, (RESOLUTION_X - bomb.get("x") * FIELD_SIZE_X,
                                                      RESOLUTION_Y - bomb.get("y") * FIELD_SIZE_Y))

    def render_end_screen(self):
        pass