import pygame

from src.frostfire.config import FLOOR_Y, HEIGHT, WIDTH


class Level1:
    """
    Simple side-scrolling level with parallax mountain layers.
    """

    def __init__(self, mountain_assets):
        self.left_bound = 0
        self.right_bound = 10000

        self.sky = pygame.Surface((WIDTH, HEIGHT))
        self.sky.fill((135, 206, 235))

        self.mountain_bg1 = mountain_assets["bg1"]
        self.mountain_bg2 = mountain_assets["bg2"]
        self.bg1_width = self.mountain_bg1.get_width()
        self.bg2_width = self.mountain_bg2.get_width()

        self.mountain_fg = mountain_assets.get("foreground")
        self.fg_width = self.mountain_fg.get_width() if self.mountain_fg else 0

        self.y_bg = HEIGHT - self.mountain_bg1.get_height() - 100
        self.y_fg = HEIGHT - self.mountain_fg.get_height() - 50 if self.mountain_fg else 0

        self.obstacles = [pygame.Rect(10000, 0, 10, HEIGHT)]

    def draw(self, screen, camera_x):
        """
        Draw background layers and level obstacles.
        """
        background_factor = 0.3
        foreground_factor = 0.65

        screen.blit(self.sky, (0, 0))

        start_x = -camera_x * background_factor
        screen.blit(self.mountain_bg1, (start_x, self.y_bg))

        x_start = start_x + self.bg1_width
        count = int((WIDTH - x_start) // self.bg2_width + 2)

        for index in range(count):
            x_position = x_start + index * self.bg2_width
            screen.blit(self.mountain_bg2, (x_position, self.y_bg))

        if self.mountain_fg:
            foreground_offset = camera_x * foreground_factor

            for index in range(-1, int(WIDTH // self.fg_width) + 2):
                x_position = index * self.fg_width - (foreground_offset % self.fg_width)
                screen.blit(self.mountain_fg, (x_position, self.y_fg))

        for obstacle in self.obstacles:
            obstacle_rect = obstacle.copy()
            obstacle_rect.x -= camera_x
            pygame.draw.rect(screen, (200, 50, 50), obstacle_rect)