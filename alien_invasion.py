import pygame
from pygame.sprite import Group

from game_functions import GameFunctions
from settings import Settings
from ship import Ship
from game_stats import GameStats


def run_game():
    pygame.init()

    ai_settings = Settings()

    screen = pygame.display.set_mode(ai_settings.screen_dim)
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    stats = GameStats(ai_settings)

    game_fun = GameFunctions(ai_settings, stats, screen, ship, aliens, bullets)

    game_fun.create_fleet()

    while True:
        game_fun.check_events()

        if stats.game_active:
            ship.update()
            game_fun.update_bullets()
            game_fun.update_aliens()

        game_fun.update_screen()


if __name__ == '__main__':
    run_game()
