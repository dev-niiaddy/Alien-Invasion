from pygame.sysfont import SysFont
from pygame import SurfaceType
import pygame

from settings import Settings


class Button:

    def __init__(self, ai_settings: Settings, screen: SurfaceType,
                 msg: str):
        self._screen = screen
        self._screen_rect = screen.get_rect()

        self._width, self._height = 200, 50
        self._button_color = (0, 255, 0)
        self._text_color = (255, 255, 255)
        self._font = SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self._width, self._height)
        self.rect.center = self._screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, message: str):
        # print(self._text_color, self._button_color, sep=" -> ")

        self._msg_image = self._font.render(message, True, self._text_color, self._button_color)

        self._msg_image_rect = self._msg_image.get_rect()
        self._msg_image_rect.center = self.rect.center

    def draw_button(self):
        self._screen.fill(self._button_color, self.rect)
        self._screen.blit(self._msg_image, self._msg_image_rect)
