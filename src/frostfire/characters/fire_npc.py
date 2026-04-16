import pygame

from src.frostfire.config import FLOOR_Y


class FireNPC:
    """
    Basic fire enemy that moves back and forth inside a fixed range.
    """

    def __init__(self, assets):
        self.assets = assets

        if self.assets.get("idle_frames"):
            image = self.assets["idle_frames"][0]
        else:
            image = self.assets["fallback"]

        self.x = 800
        self.y = FLOOR_Y - image.get_height()

        self.frame_index = 0
        self.speed = 2.5
        self.direction = -1

        self.min_x = 600
        self.max_x = 900

    def update(self, player_pos):
        """
        Update animation and horizontal movement.
        """
        if self.assets.get("idle_frames"):
            total = len(self.assets["idle_frames"])
            self.frame_index = (self.frame_index + 1) % (total * 5)

        self.x += self.speed * self.direction

        if self.x <= self.min_x:
            self.x = self.min_x
            self.direction = abs(self.direction)
        elif self.x >= self.max_x:
            self.x = self.max_x
            self.direction = -abs(self.direction)

    def draw(self, screen, camera_x):
        """
        Draw the current frame on screen.
        """
        if self.assets.get("idle_frames") and len(self.assets["idle_frames"]) > 0:
            image = self.assets["idle_frames"][self.frame_index // 5]
        else:
            image = self.assets["fallback"]

        screen.blit(image, (self.x - camera_x, self.y))

    def get_mask(self):
        """
        Return a collision mask based on the current frame.
        """
        if self.assets.get("idle_frames") and len(self.assets["idle_frames"]) > 0:
            image = self.assets["idle_frames"][self.frame_index // 5]
        else:
            image = self.assets["fallback"]

        return pygame.mask.from_surface(image)