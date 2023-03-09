import pygame
import sys
import random
from TFEgame import TFEgame

if __name__ == '__main__':
    pygame.init()

    # set up the visible screen
    pygame.display.set_caption('Taylor Swift 2048')
    WIDTH = 600
    x_center = WIDTH//2
    HEIGHT = 800
    y_center = HEIGHT//2
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    SCREEN.fill('white')

    # set up fonts
    # FONT = pygame.font.Font('tbd', 75)

    # set up clock
    CLOCK = pygame.time.Clock()

    # set up game
    DIMS = (4, 4)
    GAME = TFEgame(DIMS)
    BOARD = GAME.board()

    # set up tiles and corresponding rects
    TILE_DIM = 100
    TILE_SPACING = 10
    TILES = {(i, j): pygame.Surface((TILE_DIM, TILE_DIM)) for j in range(DIMS[1])
             for i in range(DIMS[0])}
    TILES_RECTS = {(i, j): TILES[(i, j)].get_rect(center=((x_center + (TILE_DIM+TILE_SPACING)*(j-1.5), y_center + (TILE_DIM+TILE_SPACING)*(i-1.5)))) \
                     for j in range(DIMS[1]) for i in range(DIMS[0])}


    OUTLINE_DIM = TILE_DIM*DIMS[0]+TILE_SPACING*(DIMS[0]-1)+2*TILE_SPACING
    OUTLINE = pygame.Surface((OUTLINE_DIM, OUTLINE_DIM))
    OUTLINE.fill('black')
    OUTLINE_RECT = OUTLINE.get_rect(center=(WIDTH//2, HEIGHT//2))


def blit_tiles() -> None:
    for coord in TILES:
        TILES[coord].fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        SCREEN.blit(TILES[coord], TILES_RECTS[coord])

while True:
    SCREEN.blit(OUTLINE, OUTLINE_RECT)
    blit_tiles()
    pygame.display.update()
    CLOCK.tick(60)

