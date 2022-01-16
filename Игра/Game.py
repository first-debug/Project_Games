import pygame
from os import path
from data.board import Board


SIZE = WIGHT, HEIGHT = 800, 600
FPS = 144


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_sprite)
        #  self.player_rect =


def load_image(name, colorkey=None):
    fullname = path.join('data', name)
    if not path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def settings_screen():
    #  здесь будет создаваться и отрисовываться экран настроек
    pass


def draw_game_world():
    #  создание сетки для ориентации
    board = Board(20, 15)
    #  ставим фон
    fon = load_image('fon.png')
    screen.blit(fon, (0, 0))
    #  отрисовываем землю
    GRAUND = pygame.Rect(0, 400, WIGHT, 200)
    pygame.draw.rect(screen, 'brown', GRAUND)
    #  рисуем персонажа
    pos_of_player = [320, 320]
    player_image = pygame.transform.scale(load_image('Player.png'), (40, 80))
    screen.blit(player_image, pos_of_player)
    return board, player_image, pos_of_player


def start_screen():
    intro_text = ["Mario 0.1", "", "", "", "", "", "", "", "",
                  "", "", "Настройки", "", "", "Правила игры",
                  "Чтобы продолжить нажмите Enter"]

    fon = pygame.transform.scale(load_image('fon_start_screen.jpg'), (WIGHT, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    font_of_title = pygame.font.Font(None, 60)
    text_coord = 50
    for line in intro_text:
        # разделим настройки шрифта для заголовка и подсказки
        if line != 'Mario 0.1':
            string_rendered = font.render(line, 1, pygame.Color('white'))
            string_rendered_shadow = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
        else:
            string_rendered = font_of_title.render(line, 1, pygame.Color('white'))
            string_rendered_shadow = font_of_title.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered_shadow, intro_rect.move(1, 1))
        screen.blit(string_rendered, intro_rect)
        #  находим координаты верхнего левого угла кнопки 'Настройки'
        #  в будущем может понадобиться
        print(intro_rect.topleft, line == 'Настройки')
        if line == 'Настройки':
            settings_rect = intro_rect
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    print('Перешли к игре')
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    touching = settings_rect.collidepoint(event.pos)
                    if touching:
                        settings_screen()
                        print('Перешли в настройки')
        clock.tick(FPS)


pygame.init()
screen = pygame.display.set_mode(SIZE)

player_sprite = pygame.sprite.Group()
clock = pygame.time.Clock()
start_screen()
board, player_image, pos_of_player = draw_game_world()

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            #  if event.key == pygame.K_d:
                #  pygame.draw.rect(screen, (107, 136, 254), pygame.Rect(pos_of_player, (40, 80)))
                #  pos_of_player[0] += 40
                #  screen.blit(player_image, pos_of_player)
            #  elif event.key == pygame.K_a:
                #  pygame.draw.rect(screen, '#6b88fe', pygame.Rect(pos_of_player, (40, 80)))
                #  pos_of_player[0] -= 40
                #  screen.blit(player_image, pos_of_player)
            pass
        #  отрисовываем сетку для ориентации, если нужно
    board.set_view(0, 0, 40)
    board.render(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
