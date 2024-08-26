import json


class GameStats():
    """Отслеживание статистики для игры Sky Defenders."""

    def __init__(self, sd_game):
        """Инициализирует статистику."""
        self.settings = sd_game.settings
        self.reset_stats()

        # Флаг активации игры Sky Defenders
        self.game_active = False

        self.is_shopping = False

        try:
            with open('data/save.json', 'r') as f:
                static_stats = json.load(f)
                self.record = static_stats["record"]
                self.coins = static_stats["coins"]
                self.ship_type = static_stats["ship_type"]
        except:
            self.record = 0
            self.coins = 0
            self.ship_type = "start"

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.full_ship_hp = self.settings.ship_hp
        self.score = 0
