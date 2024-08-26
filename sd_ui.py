import pygame
from pygame.sprite import Sprite


class Cloud(Sprite):
    def __init__(self, sd_game):
        """Класс управлением облаком."""
        super().__init__()

        self.screen_rect = sd_game.screen.get_rect()
        self.settings = sd_game.settings
        self.image = pygame.image.load('images/ui/cloud.png')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

        # Задача позиции
        self.rect.left = self.screen_rect.right

        # Сохранение дробных координат x
        self.x = float(self.rect.x)

    def update(self):
        """Обновление позиции облака."""
        self.x -= self.settings.cloud_speed

        if self.rect.bottom > self.screen_rect.bottom:
            self.rect.y -= 1
        if self.rect.top < self.screen_rect.top:
            self.rect.y += 1

        self.rect.x = self.x


class Button(Sprite):
    def __init__(self, sd_game, button_tag, msg, button_width, button_height, font_size=50, micro_img=None, button_color=(0, 255, 0), font_color=(255, 255, 255), msg_font=None, button_pos=(0, 0)):
        """Класс для создания кнопки."""
        super().__init__()
        self.screen = sd_game.screen
        self.color = button_color
        self.font = pygame.font.SysFont(msg_font, font_size)
        self.image = pygame.surface.Surface((button_width, button_height))
        self.rect = self.image.get_rect()
        self.msg = msg
        self.tag = button_tag
        self.micro_img = micro_img

        self.rect.center = button_pos

        self.prep_msg(font_color)
        if self.micro_img:
            self.prep_img(self.micro_img)

    def prep_msg(self, font_color):
        """Создание объекта шрифта."""
        self.msg_image = self.font.render(
            self.msg, True, font_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def prep_img(self, micro_img):
        """Создание мини иконки в кнопке"""
        self.micro_image = pygame.image.load(micro_img)
        self.micro_image.set_colorkey((255, 255, 255))
        self.micro_image_rect = self.micro_image.get_rect()
        self.micro_image_rect.centerx = self.micro_image_rect.width + \
            self.rect.centerx - (self.rect.width / 2)
        self.msg_image_rect.centerx += self.micro_image_rect.width // 2
        self.micro_image_rect.centery = self.rect.centery

    def draw_button(self):
        """Отрисовка кнопки."""
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        if self.micro_img:
            self.screen.blit(self.micro_image, self.micro_image_rect)


class HealthPoint(Sprite):
    def __init__(self, sd_game):
        """Класс отвечающий за здоровье. Не использовать в качестве основного спрайта!"""
        super().__init__()
        self.settings = sd_game.settings
        self.empty_hp_image = pygame.image.load('images/ui/empty_hp.png')
        self.full_hp_image = pygame.image.load('images/ui/full_hp.png')
        self.half_hp_image = pygame.image.load('images/ui/half_hp.png')
        self.image = self.full_hp_image
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()


class ScoreBoard():
    def __init__(self, sd_game):
        """Класс для отображения количества очков"""
        self.screen = sd_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sd_game.settings
        self.stats = sd_game.stats
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont('Franklin Gothic Demi Cond', 50)
        self.sd_game = sd_game

        self.prep_score()
        self.prep_record()
        self.prep_hp()
        self.prep_coins()

    def prep_score(self):
        """Создание и вывод очков"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = 10

    def prep_record(self):
        """Создание и вывод рекорда"""
        record_str = str(self.stats.record)
        self.record_image = self.font.render(record_str, True, self.text_color)

        self.record_rect = self.record_image.get_rect()
        self.record_rect.right = self.screen_rect.right - 200
        self.record_rect.top = 10

    def prep_hp(self):
        """Создание и вывод здоровья"""
        self.hp = pygame.sprite.Group()
        for number_hp in range(self.stats.full_ship_hp + 1):
            health_point = HealthPoint(self.sd_game)
            health_point.rect.x = 10 + number_hp * health_point.rect.width
            health_point.rect.y = 10
            self.hp.add(health_point)

    def prep_coins(self):
        """Создание и вывод монет"""
        self.coin_image = pygame.image.load('images/ui/coin.png')
        self.coin_image.set_colorkey((255, 255, 255))
        self.coin_rect = self.coin_image.get_rect()
        coins_str = str(self.stats.coins)
        self.coins_counter_image = self.font.render(coins_str, True, (255, 242, 0))
        self.coins_counter_rect = self.coins_counter_image.get_rect()

        self.coin_rect.centerx = self.screen_rect.centerx
        self.coin_rect.top = 10
        self.coins_counter_rect.centerx = self.coin_rect.centerx + (self.coin_rect.width // 2 * 3)
        self.coins_counter_rect.top = 10

    def check_record(self):
        """Проверяет нужно ли увеличивать рекорд"""
        if self.stats.score > self.stats.record:
            self.stats.record = self.stats.score
            self.prep_record()

    def draw_score(self):
        """Отрисовка всех объектов в ScoreBoard"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.record_image, self.record_rect)
        self.hp.draw(self.screen)
        self.screen.blit(self.coin_image, self.coin_rect)
        self.screen.blit(self.coins_counter_image, self.coins_counter_rect)
