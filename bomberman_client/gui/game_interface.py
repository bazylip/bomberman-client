from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


BOARD_DIMENSION_X = 15
BOARD_DIMENSION_Y = 9
RESOLUTION_X = 800
RESOLUTION_Y = 600
GRASS_COLOR = (0,255,0)
BLOCK_COLOR = (107,107,71)
FIELD_SIZE_X = RESOLUTION_X / BOARD_DIMENSION_X
FIELD_SIZE_Y = RESOLUTION_Y / BOARD_DIMENSION_Y

class GameInterface:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(size=(RESOLUTION_X, RESOLUTION_Y))
        pygame.display.set_caption("Bomberman")

    def render(self, board_state):
        self.display.fill(GRASS_COLOR)
        for block_x in range(1, 15, 2):
            for block_y in range(1, 9, 2):
                pygame.draw.rect(self.display, BLOCK_COLOR, [block_x*FIELD_SIZE_X, block_y*FIELD_SIZE_Y, FIELD_SIZE_X, FIELD_SIZE_Y])
        pygame.display.update()

    def render_end_screen(self):
        pass