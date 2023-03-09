import pygame
import sys
from TFEgame import TFEgame

if __name__ == '__main__':
    pygame.init()

    # set up the visible screen
    pygame.display.set_caption('Taylor Swift 2048')
    WIDTH = 600
    HEIGHT = 800
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    SCREEN.fill('white')

    # set up fonts
    FONT = pygame.font.Font('tbd', 75)

    # set up clock
    CLOCK = pygame.time.Clock()

    # set up game
    DIMS = (4, 4)
    GAME = TFEgame(DIMS)
    BOARD = GAME.board()

    # set up tiles and corresponding rects
    TILE_DIM = 100
    TILE_SPACING = 10

    OUTLINE = pygame.Surface(TILE_DIM*DIMS[0]+TILE_SPACING*(DIMS[0]-1))
    OUTLINE.fill('black')
    OUTLINE_RECT = OUTLINE.get_rect(center=(WIDTH//2, HEIGHT//2))
    




