from settings import Settings


class GameStats:
    ships_left: int

    def __init__(self, ai_settings: Settings):
        self.ai_settings = ai_settings
        self.reset_stats()

        self.game_active = False

        # High score should never be reset
        self.init_high_score()
        self.level = 1

    def init_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                self.high_score = int(file.read())
        except IOError:
            self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0

    def save_high_score(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))
            file.close()
