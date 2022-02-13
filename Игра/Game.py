import time

import pygame
import csv
from os import path
from random import choice
from data.board import Board

SIZE = WIDTH, HEIGHT = 960, 540
TILE_SIZE = 40
FPS = 30
BUTTON_COLOR = pygame.Color('gray')
WHITE = pygame.Color('white')

pygame.init()
pygame.mixer.music.load('data/main_menu_theme.mp3')
screen = pygame.display.set_mode(SIZE)


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


def load_settings(name):
    with open(name, encoding='utf8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for j in reader:
            if j is not None:
                return j


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, is_jump):
        super().__init__(all_sprites, player_sprite)
        self.image = pygame.transform.scale(load_image('Player.png'), (TILE_SIZE, TILE_SIZE * 2))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.jump_height = 7
        self.isJump = is_jump
        self.pos = pos

    def draw(self):
        screen.blit(self.image, self.pos)

    def jump(self):
        self.image = pygame.transform.scale(load_image('Player_jumps.png'), (TILE_SIZE, TILE_SIZE * 2))
        pygame.draw.rect(screen, '#6b88fe', self.rect)
        if self.jump_height >= -7:
            self.rect.top -= (self.jump_height * abs(self.jump_height))
            self.pos[1] = self.rect.top
            self.jump_height -= 1
        else:
            self.jump_height = 7
            self.isJump = False
            self.image = pygame.transform.scale(load_image('Player.png'), (TILE_SIZE, TILE_SIZE * 2))
        screen.blit(player.image, player.pos)



class EnemyItems(pygame.sprite.Sprite):

    def __init__(self, image, pos):
        super().__init__(all_sprites, world_sprites)
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.pos = pos
        self.rect = self.image.get_rect()

    def update(self):
        if screenRect.contains(self.rect):
            pygame.draw.rect(screen, '#6b88fe', self.rect)
            self.rect.x -= TILE_SIZE * 0.5
            if not player.rect.colliderect(self.rect):  # проверка на столкновение коробки с игроком
                screen.blit(self.image, self.rect.topleft)
            else:  # что делаем при столкновении коробки с игроком
                screen.blit(self.image, self.rect.topleft)
                end_screen()  # вызываем отрисовку экрана окончания
        else:
            pygame.draw.rect(screen, '#6b88fe', self.rect)
            self.rect.x = WIDTH - self.rect.width
            self.rect.y = choice(range(TILE_SIZE * 4, TILE_SIZE * 9, TILE_SIZE))
            screen.blit(self.image, self.rect.topleft)


class GameWorld(pygame.sprite.Sprite):

    def __init__(self, fon, flight_objects):
        super(GameWorld, self).__init__(all_sprites, world_sprites)
        self.fon = load_image(fon)
        pygame.mixer.music.load("data/main_menu_theme.mp3")
        pygame.mixer.music.play()

        #  создаём коробку
        box_image = load_image("box.png")
        pygame.transform.scale(box_image, (TILE_SIZE, TILE_SIZE))
        self.boxes = EnemyItems(box_image, (WIDTH - TILE_SIZE, choice(range(HEIGHT * 4, HEIGHT * 9))))

        #  создаём летающий фоновый объект(в наше м случае облако)
        self.flight_objects = load_image(flight_objects)
        self.flight_objects_x, self.flight_objects_y = ((WIDTH // 1.4), (HEIGHT // 5.5))
        #  создаём прямоугольник от облака
        self.fl_ob_rect = self.flight_objects.get_rect()
        self.fl_ob_rect.topleft = (self.flight_objects_x, self.flight_objects_y)

        self.ground = pygame.Rect(0, 400, WIDTH, 200)

    def draw_game_world(self):
        #  ставим фон
        pygame.mixer.music.stop()
        pygame.mixer.music.load('data/new_sound.mp3')
        screen.fill('#6b88fe')
        screen.blit(self.flight_objects, (self.flight_objects_x, self.flight_objects_y))
        #  отрисовываем землю
        pygame.draw.rect(screen, 'brown', self.ground)
        #  рисуем персонажа
        if player is not None:  # проверка для корктной отрисовки персонажа
            player.draw()

    def update(self):
        if screenRect.contains(self.fl_ob_rect):  # проверка на нахождение летающего объекта в кадре
            pygame.draw.rect(screen, '#6b88fe', self.fl_ob_rect)  # закрашиваем предыдущий кадр летающего объекта
            self.fl_ob_rect.x -= TILE_SIZE * 0.5  # изменяем положение летающего объекта
            screen.blit(self.flight_objects, self.fl_ob_rect.topleft)  # рисуем новый кадр летающего объекта
        else:
            pygame.draw.rect(screen, '#6b88fe', self.fl_ob_rect)
            self.fl_ob_rect.x = WIDTH - self.fl_ob_rect.width
            screen.blit(self.flight_objects, self.fl_ob_rect.topleft)
        self.boxes.update()


def settings_screen():
    #  осталось отредактировать отрисовку, расшифорвку кода клавиш и реализовать изменения клавиш для управления
    intro_text = ['Настройки', f'Влево          {k_left}  ', f'Вправо          {k_right}  ',
                  f'Прыжок          {k_jump}  ']

    # здесь делаем фон затемнённым
    fon = pygame.transform.scale(load_image('fon_start_screen_proba.jpg'), (WIDTH, HEIGHT))
    fon.set_alpha(90)
    screen.fill('black')
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 40)
    size_font_of_title = 60
    font_of_title = pygame.font.Font(None, size_font_of_title)
    text_coord = (HEIGHT // 3) - size_font_of_title
    anim_color = pygame.Color((50, 50, 50))

    for line in intro_text:
        # разделим настройки шрифта для заголовка и подсказки
        if line == 'Настройки':
            string_rendered = font_of_title.render(line, True, pygame.Color('white'))
            string_rendered_shadow = font_of_title.render(line, True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = (WIDTH - intro_rect.width) // 2
        else:
            string_rendered = font.render(line, True, pygame.Color('white'))
            string_rendered_shadow = font.render(line, True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 50
            intro_rect.top = text_coord
            intro_rect.x = (WIDTH - intro_rect.width) // 3
            pygame.draw.rect(screen, BUTTON_COLOR,
                             (intro_rect.x - 6, intro_rect.y - 6, 375, intro_rect.height + 12))
            pygame.draw.rect(screen, anim_color,
                             (intro_rect.x - 6, intro_rect.y - 6, 375, intro_rect.height + 12), 3)
        text_coord += intro_rect.height
        screen.blit(string_rendered_shadow, intro_rect.move(1, 1))
        screen.blit(string_rendered, intro_rect)
        if line == 'Настройки':
            settings_rect = intro_rect
        elif line == 'Играть':
            play_rect = intro_rect
        elif line == 'Правила игры':
            rules_rect = intro_rect
        elif line == 'Выход':
            exit_rect = intro_rect
    intro_text = ['Настройки звука', 'Громкость музыки', 'Громкость эффектов']

    fon = pygame.transform.scale(load_image('fon_start_screen_proba.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font_section = pygame.font.Font(None, 40)
    font_title = pygame.font.Font(None, 60)
    text_coord = 60
    anim_color = pygame.Color((50, 50, 50))
    for line in intro_text:
        if line == 'Настройки звука':
            string_rendered = font_title.render(line, 1, pygame.Color('white'))
            string_rendered_shadow = font_title.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 80
            intro_rect.top = text_coord
            intro_rect.x = (WIDTH - intro_rect.width) // 2
        else:
            string_rendered = font_section.render(line, 1, pygame.Color('white'))
            string_rendered_shadow = font_section.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 50
            intro_rect.top = text_coord
            intro_rect.x = 90
        text_coord += intro_rect.height
        screen.blit(string_rendered_shadow, intro_rect.move(1, 1))
        screen.blit(string_rendered, intro_rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    touching_settings = settings_rect.collidepoint(event.pos)
                    if touching_settings:
                        settings_screen()
                        print('Перешли в настройки')
        clock.tick(FPS)


def rules_screen():
    pass


def end_screen():
    pygame.mixer.music.load('data/main_menu_theme.mp3')
    pygame.mixer.music.play(-1)
    # all_sprites.empty() # удалим все спрайты игрового мира(в надобности пока не разобрался)
    # возварщаем коробки к левому краю экрана
    game_world.boxes.pos = (WIDTH - TILE_SIZE, choice(range(HEIGHT * 4, HEIGHT * 9)))
    game_world.boxes.rect.topleft = game_world.boxes.pos

    intro_text = ["Mario 0.1", 'Игра окончена', 'Играть снова', 'Выход в меню']

    fon = pygame.transform.scale(load_image('fon_start_screen_proba.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    font_of_end = pygame.font.Font(None, 60)
    text_coord = (HEIGHT // 3) - 60
    anim_color = pygame.Color((50, 50, 50))

    for line in intro_text:  # рендерим текст и кнопки
        # разделим настройки шрифта для заголовка и подсказки
        if line == 'Играть снова' or line == 'Выход в меню':
            string_rendered = font.render(line, True, pygame.Color('white'))
            string_rendered_shadow = font.render(line, True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 50
            intro_rect.top = text_coord
            intro_rect.x = (WIDTH - intro_rect.width) // 2
            pygame.draw.rect(screen, BUTTON_COLOR,
                             (intro_rect.x - 6, intro_rect.y - 6, intro_rect.width + 12, intro_rect.height + 12))
            pygame.draw.rect(screen, anim_color,
                             (intro_rect.x - 6, intro_rect.y - 6, intro_rect.width + 12, intro_rect.height + 12), 3)
            intro_rect.x = (WIDTH - intro_rect.width) // 2
            pygame.draw.rect(screen, BUTTON_COLOR,
                             (intro_rect.x - 6, intro_rect.y - 6, intro_rect.width + 12, intro_rect.height + 12))
            pygame.draw.rect(screen, anim_color,
                             (intro_rect.x - 6, intro_rect.y - 6, intro_rect.width + 12, intro_rect.height + 12), 3)
        elif line == 'Играть окончена':
            string_rendered = font_of_end.render(line, True, pygame.Color('white'))
            string_rendered_shadow = font_of_end.render(line, True, pygame.Color('black'))
        elif line == 'Игра окончена':
            string_rendered = font_of_end.render(line, 1, pygame.Color('white'))
            string_rendered_shadow = font_of_end.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 50
            intro_rect.top = text_coord
            intro_rect.x = (WIDTH - intro_rect.width) // 2
        else:
            string_rendered = font.render(line, True, pygame.Color('white'))
            string_rendered_shadow = font.render(line, True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 50
            intro_rect.top = text_coord
            intro_rect.x = (WIDTH - intro_rect.width) // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered_shadow, intro_rect.move(1, 1))
        screen.blit(string_rendered, intro_rect)
        if line == 'Играть снова':
            replay_rect = intro_rect
        elif line == 'Выход в меню':
            exit_menu_rect = intro_rect
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    touching_replay = replay_rect.collidepoint(event.pos)
                    touching_exit_menu_rect = exit_menu_rect.collidepoint(event.pos)
                    if touching_replay:
                        game_world.draw_game_world()
                        return
                    elif touching_exit_menu_rect:
                        start_screen()
                        return
            elif event.type == pygame.MOUSEMOTION:
                touching_replay = replay_rect.collidepoint(event.pos)
                touching_exit_menu_rect = exit_menu_rect.collidepoint(event.pos)
                if touching_replay:
                    pygame.draw.rect(screen, WHITE, (replay_rect.x - 6, replay_rect.y - 6, replay_rect.width + 12, replay_rect.height + 12), 3)
                elif touching_exit_menu_rect:
                    pygame.draw.rect(screen, WHITE, (exit_menu_rect.x - 6, exit_menu_rect.y - 6, exit_menu_rect.width + 12, exit_menu_rect.height + 12), 3)
                else:
                    pygame.draw.rect(screen, anim_color, (replay_rect.x - 6, replay_rect.y - 6, replay_rect.width + 12, replay_rect.height + 12), 3)
                    pygame.draw.rect(screen, anim_color, (exit_menu_rect.x - 6, exit_menu_rect.y - 6, exit_menu_rect.width + 12, exit_menu_rect.height + 12), 3)
                pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["Mario 0.1", 'Играть', 'Настройки', 'Правила игры', 'Выход']

    fon = pygame.transform.scale(load_image('fon_start_screen_proba.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    size_font_of_title = 60
    font_of_title = pygame.font.Font(None, size_font_of_title)
    text_coord = (HEIGHT // 3) - size_font_of_title
    anim_color = pygame.Color((50, 50, 50))

    for line in intro_text:
        # разделим настройки шрифта для заголовка и подсказки
        if line != 'Mario 0.1':
            string_rendered = font.render(line, True, pygame.Color('white'))
            string_rendered_shadow = font.render(line, True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 50
            intro_rect.top = text_coord
            intro_rect.x = (WIDTH - intro_rect.width) // 2
            pygame.draw.rect(screen, BUTTON_COLOR,
                             (intro_rect.x - 6, intro_rect.y - 6, intro_rect.width + 12, intro_rect.height + 12))
            pygame.draw.rect(screen, anim_color,
                             (intro_rect.x - 6, intro_rect.y - 6, intro_rect.width + 12, intro_rect.height + 12), 3)
        else:
            string_rendered = font_of_title.render(line, True, pygame.Color('white'))
            string_rendered_shadow = font_of_title.render(line, True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = (WIDTH - intro_rect.width) // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered_shadow, intro_rect.move(1, 1))
        screen.blit(string_rendered, intro_rect)
        #  находим координаты верхнего левого угла кнопок
        #  в будущем может понадобиться
        if line == 'Настройки':
            settings_rect = intro_rect
        elif line == 'Играть':
            play_rect = intro_rect
        elif line == 'Правила игры':
            rules_rect = intro_rect
        elif line == 'Выход':
            exit_rect = intro_rect
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    touching_settings = settings_rect.collidepoint(event.pos)
                    touching_play = play_rect.collidepoint(event.pos)
                    touching_rules = rules_rect.collidepoint(event.pos)
                    touching_exit = exit_rect.collidepoint(event.pos)
                    if touching_settings:
                        settings_screen()
                        print('Перешли в настройки')
                    elif touching_play:
                        #  добавил отрисовку игрового мира для корректной работы экрана окончания
                        game_world.draw_game_world()
                        return
                    elif touching_rules:
                        rules_screen()
                        print('Перешли в правила игры')
                    elif touching_exit:
                        pygame.quit()
            elif event.type == pygame.MOUSEMOTION:
                touching_settings = settings_rect.collidepoint(event.pos)
                touching_play = play_rect.collidepoint(event.pos)
                touching_rules = rules_rect.collidepoint(event.pos)
                touching_exit = exit_rect.collidepoint(event.pos)
                if touching_settings:
                    pygame.draw.rect(screen, WHITE, (settings_rect.x - 6, settings_rect.y - 6, settings_rect.width + 12, settings_rect.height + 12), 3)
                elif touching_play:
                    pygame.draw.rect(screen, WHITE, (play_rect.x - 6, play_rect.y - 6, play_rect.width + 12, play_rect.height + 12), 3)
                elif touching_rules:
                    pygame.draw.rect(screen, WHITE, (rules_rect.x - 6, rules_rect.y - 6, rules_rect.width + 12, rules_rect.height + 12), 3)
                elif touching_exit:
                    pygame.draw.rect(screen, WHITE, (exit_rect.x - 6, exit_rect.y - 6, exit_rect.width + 12, exit_rect.height + 12), 3)
                else:
                    pygame.draw.rect(screen, anim_color, (settings_rect.x - 6, settings_rect.y - 6, settings_rect.width + 12, settings_rect.height + 12), 3)
                    pygame.draw.rect(screen, anim_color, (play_rect.x - 6, play_rect.y - 6, play_rect.width + 12, play_rect.height + 12), 3)
                    pygame.draw.rect(screen, anim_color, (rules_rect.x - 6, rules_rect.y - 6, rules_rect.width + 12, rules_rect.height + 12), 3)
                    pygame.draw.rect(screen, anim_color, (exit_rect.x - 6, exit_rect.y - 6, exit_rect.width + 12, exit_rect.height + 12), 3)
                pygame.display.flip()
        clock.tick(FPS)


player_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
world_sprites = pygame.sprite.Group()

screenRect = screen.get_rect()

#  создание сетки для ориентации
board = Board(WIDTH // 40, HEIGHT // 40)

k_left, k_right, k_jump = load_settings('data/settings.csv')  # получаем клавиши управления

game_world = GameWorld('fon1.png', 'облочко.png')
player = Player([320, 320], False)

clock = pygame.time.Clock()

start_screen()
game_world.draw_game_world()

running = True
while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game_world.update()

    if keys[int(k_right)]:
        pygame.draw.rect(screen, '#6b88fe', player.rect)
        player.rect.left += 40
        player.pos[0] = player.rect.left
        screen.blit(player.image, player.pos)

    if keys[int(k_left)]:
        pygame.draw.rect(screen, '#6b88fe', pygame.Rect(player.pos, (40, 80)))
        player.rect.left -= 40
        player.pos[0] = player.rect.left
        screen.blit(player.image, player.pos)

    if not player.isJump:
        if keys[int(k_jump)]:
            player.isJump = True
            pygame.mixer.music.play()
    else:
        player.jump()

    #  отрисовываем сетку для ориентации, если нужно
    # board.set_view(0, 0, 40)
    # board.render(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
