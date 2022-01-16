from random import choice

import pygame
from os import path

SIZE = WIGHT, HEIGHT = 800, 600
GRAVITY = 30 / 144
# для отслеживания улетевших частиц
# удобно использовать пересечение прямоугольников
screen_rect = (0, 0, WIGHT, HEIGHT)
pygame.init()


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
        #  image = image.convert_alpha()
        pass
    return image


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers))


screen = pygame.display.set_mode(SIZE)

all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # создаём частицы по щелчку мыши
            create_particles(pygame.mouse.get_pos())

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(50)

pygame.quit()