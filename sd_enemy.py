import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    def __init__(self, sd_game):
        """Клас управления врагом"""
        super().__init__()

        self.screen_rect = sd_game.screen.get_rect()
        self.settings = sd_game.settings
        self.image = pygame.image.load('images/sprites/enemy.png')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

        # Задача позиции
        self.rect.left = self.screen_rect.right

        # Сохраннение дробных координат x
        self.x = float(self.rect.x)

    def update(self):
        """Обровление позиции врага"""
        self.x -= self.settings.enemy_speed

        if self.rect.bottom > self.screen_rect.bottom:
            self.rect.y -= 1
        if self.rect.top < self.screen_rect.top:
            self.rect.y += 1

        self.rect.x = self.x
