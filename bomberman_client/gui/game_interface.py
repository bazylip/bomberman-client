import json
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
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.display = pygame.display.set_mode(size=(RESOLUTION_X, RESOLUTION_Y))
        self.player_image1 = pygame.image.load("gui/images/player1.png").convert_alpha()
        self.player_image1 = pygame.transform.scale(self.player_image1, (50, 50))
        self.player_image2 = pygame.image.load("gui/images/player2.png").convert_alpha()
        self.player_image2 = pygame.transform.scale(self.player_image2, (50, 50))
        self.bomb_image = pygame.image.load("gui/images/bomb.png").convert_alpha()
        self.bomb_image = pygame.transform.scale(self.bomb_image, (60, 60))
        pygame.display.set_caption("Bomberman")

    def render(self, board_state_json, player_id):
        if board_state_json is not None:
            board_state = json.loads(board_state_json)
            self.display.fill(GRASS_COLOR)
            self._render_blocks()
            self._render_players(board_state)
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

    def _render_players(self, board_state):
        def render_hp(player):
            pygame.draw.rect(self.display,
                             HP_COLOR,
                             [RESOLUTION_X - player.get("x") * FIELD_SIZE_X,
                              RESOLUTION_Y - player.get("y") * FIELD_SIZE_Y + 55,
                              int(player.get("hp") / 25) * FIELD_SIZE_X/4,
                              10]
                             )


        players = [(board_state.get("player1"), 1), (board_state.get("player2"), 2)]
        for player, id in players:
            img = self.player_image1 if id == 1 else self.player_image2
            self.display.blit(img, (RESOLUTION_X - player.get("x")*FIELD_SIZE_X,
                                    RESOLUTION_Y - player.get("y")*FIELD_SIZE_Y))
            render_hp(player)

    def _render_bombs(self, board_state):
        bombs = board_state.get("bombs")
        if bombs is not None:
            for bomb in bombs:
                self.display.blit(self.bomb_image, (RESOLUTION_X - bomb.get("x") * FIELD_SIZE_X,
                                                      RESOLUTION_Y - bomb.get("y") * FIELD_SIZE_Y))

    def render_end_screen(self, id_player_won):
        self.display.fill(GRASS_COLOR)
        game_end = self.font.render(f"Game ended, player {id_player_won} won", False, (0, 0, 0))
        self.display.blit(game_end, (230, 250))
        pygame.display.update()