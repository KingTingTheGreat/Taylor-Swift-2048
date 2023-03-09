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

    # set up tile 
    # COLORS = {0:'#ffffff', 2:'#cc0001', 4:'#fb940b', 8:'#ffff01', \
    #           16:'#01cc00', 32:'#03c0c6', 64:'#0000fe', 128:'#762ca7', \
    #           256: '#fe98bf', 512: '#fe98bf', 1024: '#fe98bf', 2048: '#fe98bf'}




    # set up fonts
    FONT = pygame.font.Font('fonts\Sequoia Regular.otf', 65)

    # set up clock
    CLOCK = pygame.time.Clock()

    # set up game
    DIMS = (4, 4)
    GAME = TFEgame(DIMS)
    BOARD = GAME.board()

    # set up tiles and corresponding rects
    ALBUMS = {0: '_', 2: 'TaylorSwift', 4: 'Fearless', 8: 'SpeakNow', \
            16: 'Red', 32: '1989', 64: 'Reputation', 128: 'Lover', \
            256: 'folklore', 512: 'evermore', 1024: 'Midnights', 2048: 'ME!'}
    for val in ALBUMS:
        img = pygame.image.load(f'tiles\{ALBUMS[val]}.png').convert_alpha()
        ALBUMS[val] = pygame.transform.scale(img, (100, 100))
    TILE_DIM = 100
    TILE_SPACING = 10
    TILES_RECTS = {(i, j): ALBUMS[0].get_rect(center=((x_center + (TILE_DIM+TILE_SPACING)*(j-1.5), y_center + (TILE_DIM+TILE_SPACING)*(i-1.5)))) \
                    for j in range(DIMS[1]) for i in range(DIMS[0])}


    OUTLINE_DIM = TILE_DIM*DIMS[0]+TILE_SPACING*(DIMS[0]-1)+2*TILE_SPACING
    OUTLINE = pygame.Surface((OUTLINE_DIM, OUTLINE_DIM))
    OUTLINE.fill('black')
    OUTLINE_RECT = OUTLINE.get_rect(center=(WIDTH//2, HEIGHT//2))


def blit_title() -> None:
    title = FONT.render('Taylor Swift 2048', True, 'black')
    title_rect = title.get_rect(center=(WIDTH//2, 100))
    SCREEN.blit(title, title_rect)


def blit_score() -> None:
    score = FONT.render(f'Score: {str(GAME.score())}', True, 'black')
    score_rect = score.get_rect(center=(WIDTH//2, 700))
    SCREEN.blit(score, score_rect)


def blit_tiles(board) -> None:
    for coord in TILES_RECTS:
        # TILES[coord] = ALBUMS[board[coord]]
        SCREEN.blit(ALBUMS[board[coord]], TILES_RECTS[coord])


def blit_all() -> None:
    SCREEN.blit(OUTLINE, OUTLINE_RECT)
    blit_tiles(GAME.board())
    blit_title()
    blit_score()


def process_events(only_quit=False) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if only_quit:
            continue
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_w or key == pygame.K_UP:
                GAME.move('w')
            if key == pygame.K_a or key == pygame.K_LEFT:
                GAME.move('a')
            if key == pygame.K_s or key == pygame.K_DOWN:
                GAME.move('s')
            if key == pygame.K_d or key == pygame.K_RIGHT:
                GAME.move('d')
            if event.key == pygame.K_RETURN:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    # playing the game
    while GAME.is_playable():
        SCREEN.fill('white')
        process_events()
        blit_all()
        pygame.display.update()
        GAME.move()
        CLOCK.tick(60)

    # keeping the screen active after the game is over
    while True:
        process_events(only_quit=True)
        blit_all()
        pygame.display.update()
        CLOCK.tick(60)