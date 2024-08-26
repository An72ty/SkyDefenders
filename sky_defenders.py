import sys
import pygame
import json
import random
import sd_ui
from sd_coin import Coin
from sd_game_stats import GameStats
from sd_settings import Settings
from sd_ship import Ship
from sd_bullet import Bullet
from sd_enemy import Enemy


class SkyDefenders():
    def __init__(self):
        """Класс для управления игрой."""

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.icon = pygame.image.load('images/icon.ico')
        self.icon.set_colorkey((255, 255, 255))
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption('Sky Defenders')

        self.clock = pygame.time.Clock()
        self.myfont = pygame.font.SysFont('Franklin Gothic Demi Cond', 50)
        self.stats = GameStats(self)
        self.sb = sd_ui.ScoreBoard(self)
        self.buttons = pygame.sprite.Group()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        self._create_static_buttons()

        # Словарь с цветами кнопок магазина
        self.shops_buttons_colors = {
            "shop-quit": (0, 255, 0),
            "shop-startship10": (0, 255, 0),
            "shop-middleship20": (0, 255, 0),
            "shop-goodhip30": (0, 255, 0),
            "shop-highship40": (0, 255, 0)}

        self.missing_msg = self.myfont.render(
            "Недостаточно монет!", True, (255, 255, 255))
        self.doesnt_has_coins = False

    def run_game(self):
        """Запуск игры."""

        while True:
            self.clock.tick(self.settings.FPS)
            self.text_fps = self.myfont.render(
                f"FPS: {int(self.clock.get_fps())}", True, (255, 130, 67))
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_enemies()
                self._update_coins()

            self._check_dynamic_buttons_colors()
            self._create_dynamic_buttons()
            self._update_clouds()
            self._update_screen()

    def start_game(self):
        """Начало игры"""
        # Сброс статистики и начало игры
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.is_shopping = False

        # Сброс динамических настроек
        self.settings.initialize_dynamyc_settings()

        # Удаляет все снаряды и всех врагов
        self.bullets.empty()
        self.enemies.empty()

        # Ставит корабль в центре левой части экрана
        self.ship.center_ship()

        # Скрытие мыши
        pygame.mouse.set_visible(False)

    def _create_static_buttons(self):
        """Создание кнопок"""
        play_button = sd_ui.Button(
            self, "static-play", "Играть", 200, 50, button_pos=(self.screen.get_rect().center))
        quit_button = sd_ui.Button(self, "static-quit", "Выход", 200, 50, button_pos=(
            self.settings.screen_width // 2 + 150, self.screen.get_rect().centery + 300))
        shop_button = sd_ui.Button(self, "static-shop", "Магазин", 200, 50, button_pos=(
            self.settings.screen_width // 2 - 150, self.screen.get_rect().centery + 300))
        easy_dificult_button = sd_ui.Button(self, "static-easy", "Легко", 200, 50, button_color=(
            0, 0, 255), button_pos=(self.settings.screen_width // 4, 550))
        normal_dificult_button = sd_ui.Button(self, "static-normal", "Нормально", 200, 50, button_color=(
            0, 255, 0), button_pos=(self.settings.screen_width // 2, 550))
        hard_dificult_button = sd_ui.Button(self, "static-hard", "Сложно", 200, 50, button_color=(
            255, 0, 0), button_pos=(self.settings.screen_width // 2 + self.settings.screen_width // 4, 550))

        self.buttons.add(play_button)
        self.buttons.add(quit_button)
        self.buttons.add(shop_button)
        self.buttons.add(easy_dificult_button)
        self.buttons.add(normal_dificult_button)
        self.buttons.add(hard_dificult_button)

    def _check_dynamic_buttons_colors(self):
        if self.stats.is_shopping:
            if self.stats.ship_type == "start":
                self.shops_buttons_colors["shop-startship10"] = (60, 60, 60)
            else:
                self.shops_buttons_colors["shop-startship10"] = (0, 255, 0)

            if self.stats.ship_type == "middle":
                self.shops_buttons_colors["shop-middleship20"] = (60, 60, 60)
            else:
                self.shops_buttons_colors["shop-middleship20"] = (0, 255, 0)

            if self.stats.ship_type == "good":
                self.shops_buttons_colors["shop-goodship30"] = (60, 60, 60)
            else:
                self.shops_buttons_colors["shop-goodship30"] = (0, 255, 0)

            if self.stats.ship_type == "high":
                self.shops_buttons_colors["shop-highship40"] = (60, 60, 60)
            else:
                self.shops_buttons_colors["shop-highship40"] = (0, 255, 0)

    def _create_dynamic_buttons(self):
        """Создает динамические кнопки"""
        if self.stats.is_shopping:
            quit_shop_button = sd_ui.Button(
                self, "shop-quit", "Выход", 200, 50, button_pos=(self.settings.screen_width // 6, self.settings.screen_height // 5))
            buy_start_ship_button = sd_ui.Button(self, "shop-startship10", "10", 120, 50, button_color=self.shops_buttons_colors["shop-startship10"], micro_img='images/ui/micro_coin.png', button_pos=(
                self.settings.screen_width // 3, self.settings.screen_height // 5))
            buy_middle_ship_button = sd_ui.Button(self, "shop-middleship20", "20", 120, 50, button_color=self.shops_buttons_colors["shop-middleship20"], micro_img='images/ui/micro_coin.png', button_pos=(
                self.settings.screen_width // 3, self.settings.screen_height // 3))
            buy_good_ship_button = sd_ui.Button(self, "shop-goodship30", "30", 120, 50, button_color=self.shops_buttons_colors["shop-middleship20"], micro_img='images/ui/micro_coin.png', button_pos=(
                self.settings.screen_width // 3, self.settings.screen_height // 2))
            buy_high_ship_button = sd_ui.Button(self, "shop-highship40", "40", 120, 50, button_color=self.shops_buttons_colors["shop-middleship20"], micro_img='images/ui/micro_coin.png', button_pos=(
                self.settings.screen_width // 3, self.settings.screen_height // 2 + self.settings.screen_height // 6))

            self.buttons.add(quit_shop_button)
            self.buttons.add(buy_start_ship_button)
            self.buttons.add(buy_middle_ship_button)
            self.buttons.add(buy_good_ship_button)
            self.buttons.add(buy_high_ship_button)

    def _check_button_clicked(self, mouse_pos):
        """Проверка нажата ли какая-нибудь кнопка"""
        for button in self.buttons.sprites():
            if button.rect.collidepoint(mouse_pos):
                # Проверка нажаты ли статичные кнопки
                if not self.stats.game_active and not self.stats.is_shopping:
                    if button.tag == "static-play":
                        self.start_game()
                        self.sb.prep_score()
                        self.sb.prep_hp()
                    if button.tag == "static-quit":
                        sys.exit()
                    if button.tag == "static-shop":
                        self.stats.is_shopping = True
                    if button.tag == "static-easy":
                        self.settings.speedup_scale = 1.0014
                        self.settings.enemy_points = 40
                    if button.tag == "static-normal":
                        self.settings.speedup_scale = 1.0093
                        self.settings.enemy_points = 50
                    if button.tag == "static-hard":
                        self.settings.speedup_scale = 1.03
                        self.settings.enemy_points = 60

                # Проверка нажаты ли кнопки магазина
                if self.stats.is_shopping:
                    self._check_ship_type()
                    if button.tag == "shop-quit":
                        self.stats.is_shopping = False

                    if button.tag == "shop-startship10":
                        if self.stats.ship_type != "start":
                            if self.stats.coins >= 10:
                                self.stats.coins -= 10
                                self.sb.prep_coins()
                                self.stats.ship_type = "start"
                                self.shops_buttons_colors["shop-startship10"] = (
                                    60, 60, 60)
                                break
                            else:
                                self.doesnt_has_coins = True
                        else:
                            self.shops_buttons_colors["shop-startship10"] = (
                                60, 60, 60)

                    if button.tag == "shop-middleship20":
                        if self.stats.ship_type != "middle":
                            if self.stats.coins >= 20:
                                self.stats.coins -= 20
                                self.sb.prep_coins()
                                self.stats.ship_type = "middle"
                                self.shops_buttons_colors["shop-middleship20"] = (
                                    60, 60, 60)
                                break
                            else:
                                self.doesnt_has_coins = True
                        else:
                            self.shops_buttons_colors["shop-middleship20"] = (
                                60, 60, 60)

                    if button.tag == "shop-goodship30":
                        if self.stats.ship_type != "good":
                            if self.stats.coins >= 30:
                                self.stats.coins -= 30
                                self.sb.prep_coins()
                                self.stats.ship_type = "good"
                                self.shops_buttons_colors["shop-goodship30"] = (
                                    60, 60, 60)
                                break
                            else:
                                self.doesnt_has_coins = True
                        else:
                            self.shops_buttons_colors["shop-goodship30"] = (
                                60, 60, 60)

                    if button.tag == "shop-highship40":
                        if self.stats.ship_type != "high":
                            if self.stats.coins >= 40:
                                self.stats.coins -= 40
                                self.sb.prep_coins()
                                self.stats.ship_type = "high"
                                self.shops_buttons_colors["shop-highship40"] = (
                                    60, 60, 60)
                                break
                            else:
                                self.doesnt_has_coins = True
                        else:
                            self.shops_buttons_colors["shop-highship40"] = (
                                60, 60, 60)

    def _ship_hit(self):
        """Действия если корабль сбит."""
        if self.stats.full_ship_hp > 0:
            self.stats.full_ship_hp -= 1
            self.sb.prep_hp()
        else:
            pygame.time.wait(1000)
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_ship_type(self):
        """Проверка типа корабля"""
        if self.stats.ship_type == "start":
            self.settings.bullets_alowed = 3
            self.settings.ship_hp = 5
            self.ship.image = pygame.image.load(
                'images/sprites/start_ship.png')
            self.ship.image.set_colorkey((255, 255, 255))
            self.ship.rect = self.ship.image.get_rect()
            self.ship.center_ship()

        elif self.stats.ship_type == "middle":
            self.settings.bullets_alowed = 4
            self.settings.ship_hp = 6
            self.ship.image = pygame.image.load(
                'images/sprites/start_ship.png')
            self.ship.image.set_colorkey((255, 255, 255))
            self.ship.rect = self.ship.image.get_rect()
            self.ship.center_ship()

        else:
            pass

    def _update_bullets(self):
        """Обновление позиции снарядов"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_enemy_collisions()

    def _check_bullet_enemy_collisions(self):
        """Обработка колизий между снарядом и врагом"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.enemies, True, True)

        if collisions:
            for enemies in collisions.values():
                self.stats.score += self.settings.enemy_points * len(enemies)
            self.settings.incearse_speed()
            self.sb.prep_score()
            self.sb.check_record()

    def _fire_bullet(self):
        """Выстрел снаряда"""
        if len(self.bullets) < self.settings.bullets_alowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_enemies(self):
        """Задача позиций врагов"""
        if self.settings.spawn_enemy > 1:
            self.settings.spawn_enemy = 0
        else:
            self.settings.spawn_enemy += self.settings.time_spawn_object

            if len(self.enemies) < 4 and int(self.settings.spawn_enemy):
                enemy = Enemy(self)
                enemy.rect.y = random.randint(0, self.settings.screen_height)
                self.enemies.add(enemy)

        self.enemies.update()

        # Проверка колизий "пришелец - корабль".
        if pygame.sprite.spritecollide(self.ship, self.enemies, True):
            self._ship_hit()

        # Проверяет коснулась ли правая сторона врага левой части экрана.
        self._check_enemy_right()

    def _check_enemy_right(self):
        """Проверяет коснулась ли правая сторона врага левой части экрана."""
        screen_rect = self.screen.get_rect()
        for enemy in self.enemies.sprites():
            if enemy.rect.right <= screen_rect.left:
                self._ship_hit()
                self.enemies.remove(enemy)

    def _update_coins(self):
        """Создание и обновление позиций монет"""
        if self.settings.spawn_coin >= 1:
            self.settings.spawn_coin = 0
        else:
            self.settings.spawn_coin += self.settings.time_spawn_coin

        if len(self.coins) < 10 and int(self.settings.spawn_coin):
            new_coin = Coin(self)
            new_coin.rect.y = random.randint(0, self.settings.screen_height)

            self.coins.add(new_coin)

        for coin in self.coins.copy():
            if coin.rect.right < 0:
                self.coins.remove(coin)

        self.coins.update()

        # Проверка колизий "монета - корабль или пулей"
        self._check_coins_ship_and_bullets_collisions()

    def _check_coins_ship_and_bullets_collisions(self):
        """Проверка колизий "монета - корабль" """
        collisions_ship = pygame.sprite.spritecollide(
            self.ship, self.coins, True)
        collisions_bullets = pygame.sprite.groupcollide(
            self.bullets, self.coins, True, True)

        if collisions_ship or collisions_bullets:
            self.stats.coins += self.settings.coin_points

        self.sb.prep_coins()

    def _update_clouds(self):
        """Задача позиций облаков"""
        if self.settings.spawn_cloud >= 1:
            self.settings.spawn_cloud = 0
        else:
            self.settings.spawn_cloud += self.settings.time_spawn_object

        if len(self.clouds) < 10 and int(self.settings.spawn_cloud):
            new_cloud = sd_ui.Cloud(self)
            new_cloud.rect.y = random.randint(0, self.settings.screen_height)

            self.clouds.add(new_cloud)

        for cloud in self.clouds.copy():
            if cloud.rect.right < 0:
                self.clouds.remove(cloud)

        self.clouds.update()

    def _check_events(self):
        """Проверка событий игры."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('data/save.json', 'w') as f:
                    json.dump({"record": self.stats.record, "coins": self.stats.coins,
                              "ship_type": self.stats.ship_type}, f)
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.doesnt_has_coins = False
                mouse_pos = pygame.mouse.get_pos()
                self._check_button_clicked(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Проверка событий нажатых клавиш."""

        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            with open('data/save.json', 'w') as f:
                json.dump({"record": self.stats.record, "coins": self.stats.coins,
                          "ship_type": self.stats.ship_type}, f)
            sys.exit()
        elif event.key == pygame.K_p:
            self.start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Проверка событий отпущенных клавиш."""

        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

    def _update_screen(self):
        """Отрисовка экрана и объектов на нем."""

        self.screen.fill(self.settings.bg_color)
        self.clouds.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.enemies.draw(self.screen)
        self.coins.draw(self.screen)
        self.screen.blit(self.text_fps, (self.settings.screen_width -
                         167, self.settings.screen_height - 50))

        if self.stats.is_shopping:
            shop_bg_rect = pygame.rect.Rect(
                0, 0, self.settings.screen_width - 150, self.settings.screen_height - 150)
            shop_bg_rect.center = self.screen.get_rect().center
            self.screen.fill((80, 80, 80), shop_bg_rect)

            buy_start_ship_msg = self.myfont.render(
                "Стартовый корабль", True, (255, 255, 255))
            buy_middle_ship_msg = self.myfont.render(
                "Средний корабль", True, (255, 255, 255))
            buy_good_ship_msg = self.myfont.render(
                "Хороший корабль", True, (255, 255, 255))
            buy_high_ship_msg = self.myfont.render(
                "Лучший корабль", True, (255, 255, 255))

            self.screen.blit(
                buy_start_ship_msg, (self.settings.screen_width // 2 - 50, self.settings.screen_height // 5 - 30))
            self.screen.blit(
                buy_middle_ship_msg, (self.settings.screen_width // 2 - 50, self.settings.screen_height // 3 - 30))
            self.screen.blit(
                buy_good_ship_msg, (self.settings.screen_width // 2 - 50, self.settings.screen_height // 2 - 30))
            self.screen.blit(
                buy_high_ship_msg, (self.settings.screen_width // 2 - 50, self.settings.screen_height // 2 + self.settings.screen_height // 6 - 30))

        if not self.stats.game_active:
            for button in self.buttons.sprites():
                if "static-" in button.tag and not self.stats.is_shopping:
                    button.draw_button()
                if "shop-" in button.tag and self.stats.is_shopping:
                    button.draw_button()

        if self.doesnt_has_coins:
            self.screen.blit(self.missing_msg, (self.settings.screen_width -
                             (self.settings.screen_width - 200), self.settings.screen_height - 200))

        self.sb.draw_score()

        pygame.display.flip()


if __name__ == '__main__':
    """Создание объекта игры и ее запуск."""

    sd_game = SkyDefenders()
    sd_game.run_game()
