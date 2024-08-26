class Settings():
    def __init__(self):
        """Инициализирует статические настройки игры."""
        # Настройки экрана
        self.screen_width = 1200    # Ширина экрана
        self.screen_height = 695    # Высота экрана
        self.bg_color = (0, 204, 204)     # Цвет экрана
        self.FPS = 120    # Целевое количество кадров в секунду

        # Настройки корабля
        self.ship_hp = 5    # Здоровье коробля

        # Настройки снаряда
        self.bullet_width = 15    # Ширина снаряда
        self.bullet_height = 5    # Высота снаряда
        self.bullet_color = (70, 70, 70)    # Цвет снаряда
        self.bullets_alowed = 3     # Количество снарядов находящихся на экране одновременно

        # Параметры врага
        self.spawn_enemy = 0    # Счётчик когда должен появиться враг

        # Параметры монетки
        self.spawn_coin = 0    # Счётчик когда должна появиться монета

        # Парамеры облака
        self.spawn_cloud = 0    # Счётчик когда должно появиться облако

        self.speedup_scale = 1.0093

        self.initialize_dynamyc_settings()

    def initialize_dynamyc_settings(self):
        """Инициализирует динамические настройки игры."""
        self.ship_speed = 2.2    # Скорость корабля
        self.bullet_speed = 4.0    # Скорость снаряда
        self.enemy_speed = 2.0    # Скорость врага
        self.cloud_speed = 1.8    # Скорость облака
        self.coin_speed = 1.9    # Скорость монеты
        self.enemy_points = 50    # Количество очков которое дают за убийство врага
        self.coin_points = 1    # Количество монет которое дают за поимку монеты
        self.time_spawn_object = 0.005    # Промежуток времени между спавном обьектов
        self.time_spawn_coin = 0.001    # Промежуток времени между спавном монет

    def incearse_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.enemy_speed *= self.speedup_scale
        self.cloud_speed *= self.speedup_scale
        self.coin_speed *= self.speedup_scale
        self.time_spawn_object *= self.speedup_scale
        self.time_spawn_coin *= self.speedup_scale
