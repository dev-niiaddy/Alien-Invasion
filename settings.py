class Settings:

    def __init__(self):
        self.screen_width = 1366
        self.screen_height = 768
        self.bg_color = (0, 0, 0)
        self.screen_dim = (self.screen_width, self.screen_height)
        self.ship_speed_factor = 1.5

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255
        self.bullets_allowed = 3

        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10

        self.fleet_direction = 1
