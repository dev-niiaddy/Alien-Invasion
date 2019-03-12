from pygame.sprite import Group
from pygame.sysfont import SysFont
from pygame import SurfaceType
from settings import Settings
from game_stats import GameStats

from ship import Ship


class Scoreboard:

    def __init__(self, ai_settings: Settings, screen: SurfaceType,
                 stats: GameStats):
        self._screen = screen
        self._screen_rect = screen.get_rect()
        self._ai_settings = ai_settings
        self._stats = stats

        self._text_color = 90, 200, 50
        self._font = SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        rounded_score = int(round(self._stats.score, -1))
        score_str = "{:,}".format(rounded_score)

        self.score_image = self._font.render(score_str, True, self._text_color,
                                             self._ai_settings.bg_color)

        self._score_rect = self.score_image.get_rect()
        self._score_rect.right = self._screen_rect.right - 20
        self._score_rect.top = 20

    def prep_high_score(self):
        high_score = int(round(self._stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self._high_score_image = self._font.render(high_score_str, True, self._text_color,
                                                   self._ai_settings.bg_color)

        # Center high score at the top of the screen
        self._high_score_rect = self._high_score_image.get_rect()
        self._high_score_rect.centerx = self._screen_rect.centerx
        self._high_score_rect.top = self._score_rect.top

    def prep_level(self):
        self._level_image = self._font.render(str(self._stats.level), True, self._text_color,
                                              self._ai_settings.bg_color)

        self._level_rect = self._level_image.get_rect()
        self._level_rect.right = self._score_rect.right
        self._level_rect.top = self._score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()

        for ship_number in range(self._stats.ships_left):
            ship = Ship(self._ai_settings, self._screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        self._screen.blit(self.score_image, self._score_rect)
        self._screen.blit(self._high_score_image, self._high_score_rect)
        self._screen.blit(self._level_image, self._level_rect)
        self.ships.draw(self._screen)
