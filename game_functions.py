import sys

import pygame
from pygame import SurfaceType
from pygame.sprite import Group

from alien import Alien
from bullet import Bullet
from settings import Settings
from ship import Ship
from game_stats import GameStats
from time import sleep


class GameFunctions:

    def __init__(self, ai_settings: Settings, stats: GameStats, screen: SurfaceType,
                 ship: Ship, aliens: Group, bullets: Group):
        self._ai_settings = ai_settings
        self._stats = stats
        self._screen = screen
        self._ship = ship
        self._aliens = aliens
        self._bullets = bullets

    """Private internal methods"""

    def _fire_bullet(self):
        if len(self._bullets) < self._ai_settings.bullets_allowed:
            new_bullet = Bullet(self._ai_settings, self._screen, self._ship)
            self._bullets.add(new_bullet)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # print('Key right detected')
            self._ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self._ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self._ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self._ship.moving_left = False

    def _get_number_aliens(self, alien_width: int):
        available_space_x = self._ai_settings.screen_width - (2 * alien_width)
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    def _get_number_rows(self, ship_height: int, alien_height: int):
        available_space_y = (self._ai_settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows

    def _create_alien(self, alien_number: int, row_number: int):
        alien = Alien(self._ai_settings, self._screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self._aliens.add(alien)

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self._bullets, self._aliens, True, True)

        if len(self._aliens) == 0:
            self._bullets.empty()
            self.create_fleet()

    def _change_fleet_direction(self):
        for alien in self._aliens.sprites():
            alien.rect.y += self._ai_settings.fleet_drop_speed
        self._ai_settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        for alien in self._aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _ship_hit(self):
        if self._stats.ships_left > 0:
            self._stats.ships_left -= 1
            self._aliens.empty()
            self._bullets.empty()

            self.create_fleet()
            self._ship.center_ship()

            sleep(0.5)

        else:
            self._stats.game_active = False

    def _check_aliens_bottom(self):
        screen_rect = self._screen.get_rect()

        for alien in self._aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    """Public Methods"""

    def check_events(self):
        #  event loop for listening to user inputs
        for event in pygame.event.get():
            # print("Event type is", event.type)
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # print('Keydown detected')
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def update_bullets(self):
        self._bullets.update()

        for bullet in self._bullets.copy():
            if bullet.rect.bottom <= 0:
                self._bullets.remove(bullet)
        # print(len(bullets))
        self._check_bullet_alien_collisions()

    def create_fleet(self):
        alien = Alien(self._ai_settings, self._screen)
        alien_width = alien.rect.width
        number_aliens_x = self._get_number_aliens(alien_width)
        number_rows = self._get_number_rows(self._ship.rect.height,
                                            alien.rect.height)

        for row_number in range(number_rows):
            for alien_num in range(number_aliens_x):
                self._create_alien(alien_num, row_number)

    def update_aliens(self):
        self._check_fleet_edges()
        self._aliens.update()

        if pygame.sprite.spritecollideany(self._ship, self._aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def update_screen(self):
        # Change screen color and redraw game screen
        self._screen.fill(self._ai_settings.bg_color)
        for bullet in self._bullets.sprites():
            bullet.draw_bullet()
        self._ship.blitme()
        self._aliens.draw(self._screen)
        pygame.display.flip()
