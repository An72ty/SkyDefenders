import pygame
from pygame.sprite import Sprite


class Coin(Sprite):
    def __init__(self, sd_game):
        """Класс для создания группового объекта"""
        super().__init__()
        self.screen = sd_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sd_game.settings
        self.image = pygame.image.load('images/sprites/coin.png')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

        self.rect.left = self.screen_rect.right

        self.x = float(self.rect.x)

    def update(self):
        """Обновление позиции"""
        self.x -= self.settings.coin_speed

        self.rect.x = self.x
