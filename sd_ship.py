import pygame


class Ship():
    def __init__(self, sd_game):
        """Класс для управления кораблем."""
        self.screen = sd_game.screen
        self.screen_rect = sd_game.screen.get_rect()
        self.settings = sd_game.settings
        self.image = pygame.image.load('images/sprites/start_ship.png')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.midleft = self.screen_rect.midleft

        # Сохраняем вещественные координаты
        self.y = float(self.rect.y)

        # Флаги передвижения
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Передвижение корабля"""
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.y = self.y

    def blitme(self):
        """Отрисовка корабля"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Ставит корабль в середине левой части экрана"""
        self.rect.midleft = self.screen_rect.midleft

        self.y = float(self.rect.y)
