class Settings:

    def __init__(self):
        self.screen_width = 1366
        self.screen_height = 768
        self.bg_color = (0, 0, 0)
        self.screen_dim = (self.screen_width, self.screen_height)

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255
        self.bullets_allowed = 3

        self.fleet_drop_speed = 10

        self.speedup_scale = 1.1

        self.ship_limit = 3

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
