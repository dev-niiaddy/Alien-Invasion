import sys

import pygame
from pygame import SurfaceType
from pygame.sprite import Group

from alien import Alien
from bullet import Bullet
from settings import Settings
from ship import Ship


def check_keydown_events(event, ai_settings: Settings, screen: SurfaceType,
                         ship: Ship, bullets: Group):
    if event.key == pygame.K_RIGHT:
        # print('Key right detected')
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings: Settings, screen: SurfaceType, ship: Ship, bullets: Group):
    #  event loop for listening to user inputs
    for event in pygame.event.get():
        # print("Event type is", event.type)
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # print('Keydown detected')
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings: Settings, screen: SurfaceType, ship: Ship,
                  aliens: Group, bullets: Group):
    # Change screen color and redraw game screen
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()


def update_bullets(ai_settings: Settings, screen: SurfaceType, ship: Ship,
                   aliens: Group, bullets: Group):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings: Settings, screen: SurfaceType,
                                  ship: Ship, aliens: Group, bullets: Group):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings: Settings, screen: SurfaceType, ship: Ship,
                bullets: Group):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings: Settings, screen: SurfaceType, ship: Ship, aliens: Group):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    for row_number in range(number_rows):
        for alien_num in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_num, row_number)


def get_number_aliens(ai_settings: Settings, alien_width: int):
    print('Screen width', ai_settings.screen_width)
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings: Settings, ship_height: float, alien_height):
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings: Settings, screen: SurfaceType, aliens: Group,
                 alien_number: int, row_number: int):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def update_aliens(ai_settings: Settings, aliens: Group):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()


def check_fleet_edges(ai_settings: Settings, aliens: Group):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings: Settings, aliens: Group):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1