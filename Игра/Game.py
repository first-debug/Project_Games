import pygame
from os import path
from random import choice
from data.board import Board

SIZE = WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
FPS = 30
BUTTON_COLOR = pygame.Color('gray')

pygame.init()
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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, isJump):
        super().__init__(all_sprites, player_sprite)
        self.image = pygame.transform.scale(load_image('Player.png'), (TILE_SIZE, TILE_SIZE * 2))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.jump_height = 7
        self.isJump = isJump
        self.pos = pos

    def draw(self):
        screen.blit(self.image, self.pos)

    def jump(self):
        pygame.draw.rect(screen, '#6b88fe', self.rect)
        if self.jump_height >= -7:
            self.rect.top -= (self.jump_height * abs(self.jump_height))
            self.pos[1] = self.rect.top
            self.jump_height -= 1
        else:
            self.jump_height = 7
            self.isJump = False
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
                print('GG')
        else:
            pygame.draw.rect(screen, '#6b88fe', self.rect)
            self.rect.x = WIDTH - self.rect.width
            self.rect.y = choice(range(TILE_SIZE * 4, TILE_SIZE * 9, TILE_SIZE))
            screen.blit(self.image, self.rect.topleft)


class GameWorld(pygame.sprite.Sprite):

    def __init__(self, fon, flight_objects):
        super(GameWorld, self).__init__(all_sprites, world_sprites)
        self.fon = load_image(fon)

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
        screen.fill('#6b88fe')
        screen.blit(self.flight_objects, (self.flight_objects_x, self.flight_objects_y))
        #  отрисовываем землю
        pygame.draw.rect(screen, 'brown', self.ground)
        #  рисуем персонажа
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
    #  здесь будет создаваться и отрисовываться экран настроек
    pass


def rules_screen():
    # здесь будет создаваться и отрисовываться экран правил
    pass


def start_screen():
    intro_text = ["Mario 0.1", 'Играть', 'Настройки', 'Правила игры']

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
            string_rendered = font.render(line, 1, pygame.Color('white'))
            string_rendered_shadow = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 50
            intro_rect.top = text_coord
            intro_rect.x = (WIDTH - intro_rect.width) // 2
            pygame.draw.rect(screen, BUTTON_COLOR,
                             (intro_rect.x - 6, intro_rect.y - 6, intro_rect.width + 12, intro_rect.height + 12))
            pygame.draw.rect(screen, anim_color, (intro_rect.x - 6, intro_rect.y - 6, intro_rect.width + 12, intro_rect.height + 12), 3)
            intro_rect.x = (WIDTH - intro_rect.width) // 2
            pygame.draw.rect(screen, BUTTON_COLOR,
                             (intro_rect.x - 6, intro_rect.y - 6, intro_rect.width + 12, intro_rect.height + 12))
            pygame.draw.rect(screen, anim_color,
                             (intro_rect.x - 6, intro_rect.y - 6, intro_rect.width + 12, intro_rect.height + 12), 3)
        else:
            string_rendered = font_of_title.render(line, 1, pygame.Color('white'))
            string_rendered_shadow = font_of_title.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = (WIDTH - intro_rect.width) // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered_shadow, intro_rect.move(1, 1))
        screen.blit(string_rendered, intro_rect)
        #  находим координаты верхнего левого угла кнопок
        #  в будущем может понадобиться
        print(intro_rect.topleft, line == 'Настройки')
        if line == 'Настройки':
            settings_rect = intro_rect
        elif line == 'Играть':
            play_rect = intro_rect
        elif line == 'Правила игры':
            rules_rect = intro_rect
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
                    if touching_settings:
                        settings_screen()
                        print('Перешли в настройки')
                    elif touching_play:
                        return
                    elif touching_rules:
                        rules_screen()
                        print('Перешли в правила игры')
        clock.tick(FPS)


player_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
world_sprites = pygame.sprite.Group()

screenRect = screen.get_rect()

#  создание сетки для ориентации
board = Board(WIDTH // 40, HEIGHT // 40)

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

    if keys[pygame.K_d]:
        pygame.draw.rect(screen, '#6b88fe', player.rect)
        player.rect.left += 40
        player.pos[0] = player.rect.left
        screen.blit(player.image, player.pos)

    if keys[pygame.K_a]:
        pygame.draw.rect(screen, '#6b88fe', pygame.Rect(player.pos, (40, 80)))
        player.rect.left -= 40
        player.pos[0] = player.rect.left
        screen.blit(player.image, player.pos)

    if not player.isJump:
        if keys[pygame.K_SPACE]:
            player.isJump = True
    else:
        player.jump()

    #  отрисовываем сетку для ориентации, если нужно
    # board.set_view(0, 0, 40)
    # board.render(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
