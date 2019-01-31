from settings import Settings


class GameStats:
    ships_left: int

    def __init__(self, ai_settings: Settings):
        self.ai_settings = ai_settings
        self.reset_stats()

        self.game_active = False

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
