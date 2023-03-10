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
    FONT = pygame.font.Font('fonts\Sequoia Regular.otf', 65)
    GAMEOVER_FONT = pygame.font.Font('fonts\OpenSans-ExtraBold.ttf', 80)

    # set up clock
    CLOCK = pygame.time.Clock()

    # set up game
    DIMS = (4, 4)
    GAME = TFEgame(DIMS)
    BOARD = GAME.board()

    # set up tile images and corresponding rects
    ALBUMS = {0: '_', 2: 'TaylorSwift', 4: 'Fearless', 8: 'SpeakNow', \
            16: 'Red', 32: '1989', 64: 'Reputation', 128: 'Lover', \
            256: 'folklore', 512: 'evermore', 1024: 'Midnights', 2048: 'END'}
    ALBUM_IMAGES = {}
    for val in ALBUMS:
        album = ALBUMS[val]
        if album == 'END':
            album = 'ME!'
        img = pygame.image.load(f'tiles\{album}.png').convert_alpha()
        ALBUM_IMAGES[val] = pygame.transform.scale(img, (100, 100))
    TILE_DIM = 100
    TILE_SPACING = 10
    TILES_RECTS = {(i, j): ALBUM_IMAGES[0].get_rect(center=((x_center + (TILE_DIM+TILE_SPACING)*(j-1.5), y_center + (TILE_DIM+TILE_SPACING)*(i-1.5)))) \
                    for j in range(DIMS[1]) for i in range(DIMS[0])}

    # set up outline of tiles
    OUTLINE_DIM = TILE_DIM*DIMS[0]+TILE_SPACING*(DIMS[0]-1)+2*TILE_SPACING
    OUTLINE = pygame.Surface((OUTLINE_DIM, OUTLINE_DIM))
    OUTLINE.fill('black')
    OUTLINE_RECT = OUTLINE.get_rect(center=(WIDTH//2, HEIGHT//2))

    # set up song
    current_song = ALBUMS[GAME.max_tile()]  # song will either be from TaylorSwift or from Fearless
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.load(f'songs\{current_song}.mp3')
    pygame.mixer.music.play()


def blit_title() -> None:
    """ blits the title """
    title = FONT.render('Taylor Swift 2048', True, 'black')
    title_rect = title.get_rect(center=(WIDTH//2, 100))
    SCREEN.blit(title, title_rect)


def blit_score() -> None:
    """ blits the score """
    score = FONT.render(f'Score: {str(GAME.score())}', True, 'black')
    score_rect = score.get_rect(center=(WIDTH//2, 700))
    SCREEN.blit(score, score_rect)


def blit_tiles(board) -> None:
    """ blits the tiles of the board """
    for coord in TILES_RECTS:
        SCREEN.blit(ALBUM_IMAGES[board[coord]], TILES_RECTS[coord])


def blit_all() -> None:
    """ blits all the elements of the game """
    SCREEN.fill('white')
    SCREEN.blit(OUTLINE, OUTLINE_RECT)
    blit_tiles(GAME.board())
    blit_title()
    blit_score()


def blit_gameover() -> None:
    """ blits the gameover message """
    gameover = GAMEOVER_FONT.render('GAME OVER', True, 'red')
    gameover_rect = gameover.get_rect(center=(WIDTH//2, 400))
    SCREEN.blit(gameover, gameover_rect)


def blit_loss(current_song) -> None:
    counter = 0
    while True:
        process_events(only_quit=True)
        current_song = play_song(current_song)
        blit_all()
        if counter < 15:
            blit_gameover()
        if counter >= 30:
            counter = 0
        counter += 1
        pygame.display.update()
        CLOCK.tick(60)


def blit_won(current_song) -> None:
    counter = 0
    while True:
        process_events(only_quit=True)
        current_song = play_song(current_song)
        blit_all()
        if counter < 15:
            blit_gameover()
        if counter >= 30:
            counter = 0
        counter += 1
        pygame.display.update()
        CLOCK.tick(60)


def play_song(current_song) -> str:
    """ plays the song corresponding to the current max score """
    next_song = ALBUMS[GAME.max_tile()]
    if current_song == '_' or current_song == next_song:
        return current_song
    current_song = next_song
    if current_song == 'END':
        current_song = 'ME!'
    pygame.mixer.music.load(f'songs\{current_song}.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
    return current_song


def process_events(only_quit=False) -> None:
    """ processes events 
    only_quit: if True, only the quit event is processed """
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
            elif key == pygame.K_a or key == pygame.K_LEFT:
                GAME.move('a')
            elif key == pygame.K_s or key == pygame.K_DOWN:
                GAME.move('s')
            elif key == pygame.K_d or key == pygame.K_RIGHT:
                GAME.move('d')
            elif event.key == pygame.K_RETURN:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    # playing the game
    while GAME.is_playable():
        process_events()
        current_song = play_song(current_song)
        blit_all()
        pygame.display.update()
        CLOCK.tick(60)

    print('game over')
    # keeping the screen active after the game is over
    if GAME.won():
        blit_won(current_song)
    else:
        blit_loss(current_song)