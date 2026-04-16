import pygame

from src.frostfire.config import FLOOR_Y


class IceFireNPC:
    """
    Enemy with idle and death animations.
    Can be defeated by jumping on top of it.
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
        self.speed = 3
        self.direction = -1
        self.dead = False
        self.finished = False

        self.min_x = 600
        self.max_x = 900

    def kill(self):
        """
        Trigger the death animation.
        """
        self.dead = True
        self.frame_index = 0

    def update(self, player_pos):
        """
        Update animation and movement.
        """
        if self.dead:
            if self.assets.get("dead_frames"):
                total = len(self.assets["dead_frames"])
                self.frame_index += 1
                if self.frame_index // 5 >= total:
                    self.finished = True
        else:
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
        Draw either the idle frame or the death frame.
        """
        if self.dead:
            if self.assets.get("dead_frames") and len(self.assets["dead_frames"]) > 0:
                index = self.frame_index // 5
                if index >= len(self.assets["dead_frames"]):
                    index = len(self.assets["dead_frames"]) - 1
                image = self.assets["dead_frames"][index]
            else:
                image = self.assets["fallback"]
        else:
            if self.assets.get("idle_frames") and len(self.assets["idle_frames"]) > 0:
                image = self.assets["idle_frames"][self.frame_index // 5]
            else:
                image = self.assets["fallback"]

        screen.blit(image, (self.x - camera_x, self.y))

    def get_mask(self):
        """
        Return a collision mask for the current frame.
        """
        if self.dead:
            if self.assets.get("dead_frames") and len(self.assets["dead_frames"]) > 0:
                index = self.frame_index // 5
                if index >= len(self.assets["dead_frames"]):
                    index = len(self.assets["dead_frames"]) - 1
                image = self.assets["dead_frames"][index]
            else:
                image = self.assets["fallback"]
        else:
            if self.assets.get("idle_frames") and len(self.assets["idle_frames"]) > 0:
                image = self.assets["idle_frames"][self.frame_index // 5]
            else:
                image = self.assets["fallback"]

        return pygame.mask.from_surface(image)