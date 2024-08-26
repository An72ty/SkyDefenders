import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, sd_game):
        """Класс управления снарядом."""
        super().__init__()
        self.screen = sd_game.screen
        self.settings = sd_game.settings
        self.color = sd_game.settings.bullet_color
        self.rect = pygame.Rect(
            (0, 0), (self.settings.bullet_width, self.settings.bullet_height))

        self.x = float(self.rect.x)

        self.rect.midright = sd_game.ship.rect.midright

    def update(self):
        """Передвижение снаряда"""
        self.x += self.settings.bullet_speed

        self.rect.x = self.x

    def draw_bullet(self):
        """Отрисовка снаряда"""
        pygame.draw.rect(self.screen, self.color, self.rect)
