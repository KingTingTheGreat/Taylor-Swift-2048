import pygame
import sys
import numpy as np
from TFEgame import TFEgame
from pyvidplayer import Video

if __name__ == '__main__':
    pygame.init()

    # set up the visible screen
    pygame.display.set_caption('Taylor Swift 2048')
    WIDTH:int = 600
    x_center:int = WIDTH//2
    HEIGHT:int = 800
    y_center:int = HEIGHT//2
    SCREEN:pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    SCREEN.fill('white')

    # set up fonts
    FONT:pygame.font.Font = pygame.font.Font('fonts\Sequoia Regular.otf', 65)
    GAMEOVER_FONT:pygame.font.Font = pygame.font.Font('fonts\OpenSans-ExtraBold.ttf', 80)

    # set up clock
    CLOCK:pygame.time.Clock = pygame.time.Clock()
    FPS:int = 60

    # set up game
    DIMS:tuple[int] = (4, 4)
    GAME:TFEgame = TFEgame(DIMS)
    BOARD:np.array = GAME.board()

    # set up tile images and corresponding rects
    ALBUMS:dict[int, str] = {0: '_', 2: 'TaylorSwift', 4: 'Fearless', 8: 'SpeakNow', \
            16: 'Red', 32: '1989', 64: 'Reputation', 128: 'Lover', \
            256: 'folklore', 512: 'evermore', 1024: 'Midnights', 2048: 'END'}
    ALBUM_IMAGES:dict[int, pygame.Surface] = {}
    for key in ALBUMS:
        album = ALBUMS[key]
        if album == 'END':
            album = 'ME!'
        img = pygame.image.load(f'tiles\{album}.png').convert_alpha()
        ALBUM_IMAGES[key] = pygame.transform.scale(img, (100, 100))
    TILE_DIM:int = 100
    TILE_SPACING:int = 10
    TILES_RECTS:dict[tuple[int, int], any] = {(i, j): ALBUM_IMAGES[0].get_rect(center=((x_center + (TILE_DIM+TILE_SPACING)*(j-1.5), \
                                                             y_center + (TILE_DIM+TILE_SPACING)*(i-1.5)))) \
                    for j in range(DIMS[1]) for i in range(DIMS[0])}

    # set up outline of tiles
    OUTLINE_DIM:int = TILE_DIM*DIMS[0]+TILE_SPACING*(DIMS[0]-1)+2*TILE_SPACING
    OUTLINE:pygame.Surface = pygame.Surface((OUTLINE_DIM, OUTLINE_DIM))
    OUTLINE.fill('black')
    OUTLINE_RECT:pygame.Rect = OUTLINE.get_rect(center=(WIDTH//2, HEIGHT//2))
    OUTLINE_VERT = pygame.Surface((TILE_SPACING, OUTLINE_DIM))
    OUTLINE_VERT.fill('black')
    OUTLINE_HORIZ = pygame.Surface((OUTLINE_DIM, TILE_SPACING))
    OUTLINE_HORIZ.fill('black')


    # set up music video
    current_video:Video = Video(f'music-videos/{ALBUMS[GAME.max_tile()]}.mp4')
    VIDEO_COORDS:tuple[int] = (0, HEIGHT//4)


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
        # print(ALBUM_IMAGES)
        # print(TILES_RECTS)
        SCREEN.blit(ALBUM_IMAGES[board[coord]], TILES_RECTS[coord])


def blit_outline() -> None:
    """ blits the outline of the tiles """
    for i in range(DIMS[0]+1):
        SCREEN.blit(OUTLINE_VERT, (OUTLINE_RECT.left + (TILE_DIM+TILE_SPACING)*i, OUTLINE_RECT.top))
    for j in range(DIMS[1]+1):
        SCREEN.blit(OUTLINE_HORIZ, (OUTLINE_RECT.left, OUTLINE_RECT.top + (TILE_DIM+TILE_SPACING)*j))


def blit_all(current_video=None) -> None:
    """ blits all the elements of the game """
    SCREEN.fill('white')
    if current_video:
        current_video.draw(SCREEN, VIDEO_COORDS, force_draw=True)
    # SCREEN.blit(OUTLINE, OUTLINE_RECT)
    blit_outline()
    blit_tiles(GAME.board())
    blit_title()
    blit_score()


def blit_gameover() -> None:
    """ blits the gameover message """
    gameover = GAMEOVER_FONT.render('GAME OVER', True, 'red')
    gameover_rect = gameover.get_rect(center=(WIDTH//2, HEIGHT//2))
    SCREEN.blit(gameover, gameover_rect)


def blit_loss(current_song) -> None:
    counter = 0
    while True:
        process_events(only_quit=True)
        current_song = play_song(current_song)
        blit_all()
        if counter < FPS//4:
            blit_gameover()
        if counter >= FPS//2:
            counter = 0
        counter += 1
        pygame.display.update()
        CLOCK.tick(FPS)


def blit_winner() -> None:
    """ blits the winner message """
    winner = GAMEOVER_FONT.render('YOU WIN!', True, 'green')
    winner_rect = winner.get_rect(center=(WIDTH//2, HEIGHT//2))
    SCREEN.blit(winner, winner_rect)


def blit_won(current_song) -> None:
    img_dim = TILE_DIM*DIMS[0]+TILE_SPACING*(DIMS[0]-1)
    img = pygame.image.load('tiles\ME!.png').convert_alpha()
    img = pygame.transform.scale(img, (img_dim, img_dim))
    counter = 0
    while True:
        process_events(only_quit=True)
        current_song = play_song(current_song)
        blit_all()
        if counter < FPS//4:
            SCREEN.blit(img, (WIDTH//2-img_dim//2, HEIGHT//2-img_dim//2))
            blit_winner()
        if counter >= FPS//2:
            counter = 0
        counter += 1
        pygame.display.update()
        CLOCK.tick(FPS)


def play_song(current_song) -> any:
    """ plays the song corresponding to the current max score """
    next_song = ALBUMS[GAME.max_tile()]
    if current_song == '_' or current_song.path == f'music-videos/{next_song}.mp4':
        return None
    if next_song == 'END':
        next_song = 'ME!'
    return Video(f'music-videos/{next_song}.mp4')


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
        # current_song = play_song(current_song)
        next_song = play_song(current_video)
        if next_song:
            current_video = next_song
        blit_all(current_video)
        pygame.display.update()
        CLOCK.tick(FPS)

    # # keeping the screen active after the game is over
    # if GAME.won():
    #     blit_won(current_song)
    # else:
    #     blit_loss(current_song)