import pygame
from os import path
from data.board import Board

SIZE = WIDTH, HEIGHT = 1000, 600
FPS = 30


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, isJump):
        super().__init__(all_sprites, player_sprite)
        self.image = pygame.transform.scale(load_image('Player.png'), (40, 80))
        self.jump_height = 7
        self.isJump = isJump
        self.pos = pos

    def draw(self):
        screen.blit(self.image, self.pos)

    def jump(self):
        pygame.draw.rect(screen, '#6b88fe', pygame.Rect(player.pos, (40, 80)))
        if self.jump_height >= -7:
            self.pos[1] -= (self.jump_height * abs(self.jump_height)) * 0.5
            self.jump_height -= 1
        else:  # This will execute if our jump is finished
            self.jump_height = 7
            self.isJump = False
        screen.blit(player.image, player.pos)


class GameWorld(pygame.sprite.Sprite):

    def __init__(self, fon, flight_objects):
        self.fon = load_image(fon)
        self.flight_objects = load_image(flight_objects)
        self.ground = pygame.Rect(0, 400, WIDTH, 200)
        super(GameWorld, self).__init__(all_sprites, world_sprites)

    def draw_game_world(self):
        #  ставим фон
        screen.fill('#6b88fe')
        screen.blit(self.flight_objects, ((WIDTH // 1.4), (HEIGHT // 5.5)))
        #  отрисовываем землю
        pygame.draw.rect(screen, 'brown', self.ground)
        #  рисуем персонажа
        player.draw()


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
    fon = pygame.transform.scale(load_image('fon_start_screen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    size_title_font = 60
    title_font = pygame.font.Font(None, size_title_font)
    text_coord = 50

    size_sections_font = 40
    sections_font = pygame.font.Font(None, size_sections_font)

    settings_text = ['Настройки', 'Громкость', 'Клавиши', 'Эффекты', 'Музыка']

    for line in settings_text:
        if line == 'Настройки':
            string_rendered = title_font.render(line, 1, pygame.Color('white'))
            string_rendered_shadow = title_font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 50
            intro_rect.top = text_coord
            intro_rect.x = (WIDTH - intro_rect.width) // 2
        elif line == 'Громкость' or line == 'Клавиши':

        text_coord += intro_rect.height
        screen.blit(string_rendered_shadow, intro_rect.move(1, 1))
        screen.blit(string_rendered, intro_rect)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_screen()
                    running = False
        clock.tick(FPS)


def rules_screen():
    # здесь будет создаваться и отрисовываться экран правил
    pass


def start_screen():
    intro_text = ["Mario 0.1", 'Играть', 'Настройки', 'Правила игры']

    fon = pygame.transform.scale(load_image('fon_start_screen.jpg'), (WIDTH, HEIGHT))
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
    running = True
    while running:
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

pygame.init()

screen = pygame.display.set_mode(SIZE)

all_sprites = pygame.sprite.Group()
world_sprites = pygame.sprite.Group()

player_sprite = pygame.sprite.Group()
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
            if keys[pygame.K_d]:
                pygame.draw.rect(screen, '#6b88fe', pygame.Rect(player.pos, (40, 80)))
                player.pos[0] += 40
                screen.blit(player.image, player.pos)
            if keys[pygame.K_a]:
                pygame.draw.rect(screen, '#6b88fe', pygame.Rect(player.pos, (40, 80)))
                player.pos[0] -= 40
                screen.blit(player.image, player.pos)

            if not player.isJump:
                if keys[pygame.K_SPACE]:
                    player.isJump = True
            else:
                # This is what will happen if we are jumping
                player.jump()
    board.set_view(0, 0, 40)
    board.render(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
