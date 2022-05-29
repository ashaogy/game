import pygame
from constants import *

# Этот класс описывает управление и поведение спрайта игрока
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, img='noname girl.png'):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('noname girl.png'))
        self.sprites.append(pygame.image.load('heart.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        # Положение спрайта игрока на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        # Скорость игрока по x и по y
        self.change_x = 0
        self.change_y = 0
        self.platforms = pygame.sprite.Group()
        self.artifacts = pygame.sprite.Group()
        self.score = 0
        self.lives = 5

    def update(self):

        self.calc_grav()

        self.rect.x += self.change_x

        # Проверка столкновение с препятствием
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        # Проверка столкновение с препятствием
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

        # Проверка столкновение с артефактом
        artifact_hit_list = pygame.sprite.spritecollide(self, self.artifacts, False)
        for artifact in artifact_hit_list:
            self.score += 1
            artifact.kill()

    # Расчет гравитации
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            # Ускорение свободного падения:
            self.change_y += .35

        # Проверка: персонаж на земле или нет
        if self.rect.y >= WIN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = WIN_HEIGHT - self.rect.height

        # Проверка: выход за границу экрана
        if self.rect.x < 0:
            self.rect.x = 0
            self.change_x = 0

    # Вызывается, когда пользователь нажимает на кнопку прыжок
    def jump(self):

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 2
        # Увеличиваем скорость, если прыгает
        if len(platform_hit_list) > 0 or self.rect.bottom >= WIN_HEIGHT:
            self.change_y = -10

    # Движение контролируемое игроком:
    def go_left(self):
        # Когда пользователь жмёт на лево
        self.change_x = -6

    def go_right(self):
        # Когда пользователь жмёт на право
        self.change_x = 6

    def stop(self):
        # Когда пользователь отпустил клавиатуру
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    images = ['cloud.png']

    # Препятствия, по которым моежт перемещаться персонаж, НЕ СКВОЗЬ НИХ
    def __init__(self, x, y, type):
        super().__init__()
        self.image = pygame.image.load(Platform.images[0]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


# Класс Artifact это клубника (артефакт), который нужен для сбора
class Artifact(pygame.sprite.Sprite):
    def __init__(self, x, y, img='berry.png'):
        super().__init__()
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


# Класс Enemy описывает противника персонажа
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, img='mushroom.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start = x
        self.stop = x
        self.direction = 1
        self.speed = 2

    def shift(self, x):
        self.rect.x += x
        self.start += x
        self.stop += x

    def update(self):
        if self.rect.x >= self.stop:
            self.rect.x = self.stop
            self.direction = -1
        if self.rect.x <= self.start:
            self.rect.x = self.start
            self.direction = 1
        self.rect.x += self.direction * self.speed
