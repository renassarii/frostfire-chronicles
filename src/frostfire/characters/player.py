import pygame

from src.frostfire.config import (
    CROUCH_ANIMATION_SPEED,
    GENERAL_ANIMATION_SPEED,
    HEIGHT,
    JUMP_HEIGHT,
    UNCROUCH_ANIMATION_SPEED,
    WIDTH,
)


class Player:
    """
    Player character with movement, jump, crouch, and animation handling.
    """

    def __init__(self, assets):
        self.assets = assets
        self.image = assets["static_right"]
        self.rect = self.image.get_rect()

        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT - self.rect.height - 50

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.frame_index = 0
        self.jumping = False
        self.jump_progress = 0
        self.animate = False
        self.moving_left = False
        self.speed = 5

        self.last_direction = "right"
        self.crouch_state = "idle"

    def handle_input(self, keys):
        """
        Process keyboard input and update player state.
        """
        if keys[pygame.K_a]:
            self.last_direction = "left"

        if keys[pygame.K_d]:
            self.last_direction = "right"

        if keys[pygame.K_s]:
            if self.crouch_state == "idle":
                self.crouch_state = "crouching"
                self.frame_index = 0
        else:
            if self.crouch_state == "crouched":
                self.crouch_state = "uncrouching"
                self.frame_index = 0

        if self.crouch_state == "idle":
            if keys[pygame.K_a]:
                self.x -= self.speed
                self.animate = True
                self.moving_left = True
            elif keys[pygame.K_d]:
                self.x += self.speed
                self.animate = True
                self.moving_left = False
            else:
                self.animate = False

            if keys[pygame.K_w] and not self.jumping:
                self.jumping = True
                self.jump_progress = JUMP_HEIGHT
                self.frame_index = 0

        if self.jumping:
            self.y -= self.jump_progress // 6
            self.jump_progress -= 5

            if self.jump_progress <= -JUMP_HEIGHT:
                self.jumping = False
                self.jump_progress = 0
                self.y = HEIGHT - self.rect.height - 50
                self.frame_index = 0

    def update(self, keys):
        """
        Update input, animation, and rectangle position.
        """
        self.handle_input(keys)
        self.update_animation()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update_animation(self):
        """
        Update the displayed sprite based on the current player state.
        """
        if self.crouch_state == "crouching":
            if self.last_direction == "left" and self.assets.get("crouch_left_frames"):
                self.frame_index += 1
                total = len(self.assets["crouch_left_frames"]) * CROUCH_ANIMATION_SPEED

                if self.frame_index >= total:
                    self.frame_index = 0
                    self.crouch_state = "crouched"
                    self.image = self.assets["crouched_left"]
                else:
                    self.image = self.assets["crouch_left_frames"][
                        self.frame_index // CROUCH_ANIMATION_SPEED
                    ]

            elif self.last_direction == "right" and self.assets.get("crouch_right_frames"):
                self.frame_index += 1
                total = len(self.assets["crouch_right_frames"]) * CROUCH_ANIMATION_SPEED

                if self.frame_index >= total:
                    self.frame_index = 0
                    self.crouch_state = "crouched"
                    self.image = self.assets["crouched_right"]
                else:
                    self.image = self.assets["crouch_right_frames"][
                        self.frame_index // CROUCH_ANIMATION_SPEED
                    ]
            else:
                self.crouch_state = "crouched"
                self.image = (
                    self.assets["crouched_left"]
                    if self.last_direction == "left"
                    else self.assets["crouched_right"]
                )

        elif self.crouch_state == "crouched":
            self.image = (
                self.assets["crouched_left"]
                if self.last_direction == "left"
                else self.assets["crouched_right"]
            )

        elif self.crouch_state == "uncrouching":
            if self.last_direction == "left" and self.assets.get("uncrouch_left_frames"):
                self.frame_index += 1
                total = len(self.assets["uncrouch_left_frames"]) * UNCROUCH_ANIMATION_SPEED

                if self.frame_index >= total:
                    self.frame_index = 0
                    self.crouch_state = "idle"
                    self.image = self.assets["static_left"]
                else:
                    self.image = self.assets["uncrouch_left_frames"][
                        self.frame_index // UNCROUCH_ANIMATION_SPEED
                    ]

            elif self.last_direction == "right" and self.assets.get("uncrouch_right_frames"):
                self.frame_index += 1
                total = len(self.assets["uncrouch_right_frames"]) * UNCROUCH_ANIMATION_SPEED

                if self.frame_index >= total:
                    self.frame_index = 0
                    self.crouch_state = "idle"
                    self.image = self.assets["static_right"]
                else:
                    self.image = self.assets["uncrouch_right_frames"][
                        self.frame_index // UNCROUCH_ANIMATION_SPEED
                    ]
            else:
                self.crouch_state = "idle"
                self.image = (
                    self.assets["static_left"]
                    if self.last_direction == "left"
                    else self.assets["static_right"]
                )

        elif self.jumping:
            if self.last_direction == "right" and self.assets.get("jump_right_frames"):
                total = len(self.assets["jump_right_frames"]) * GENERAL_ANIMATION_SPEED
                if self.frame_index < total - 1:
                    self.frame_index += 1
                self.image = self.assets["jump_right_frames"][
                    self.frame_index // GENERAL_ANIMATION_SPEED
                ]

            elif self.last_direction == "left" and self.assets.get("jump_left_frames"):
                total = len(self.assets["jump_left_frames"]) * GENERAL_ANIMATION_SPEED
                if self.frame_index < total - 1:
                    self.frame_index += 1
                self.image = self.assets["jump_left_frames"][
                    self.frame_index // GENERAL_ANIMATION_SPEED
                ]

            elif self.assets.get("jump_frames"):
                total = len(self.assets["jump_frames"]) * GENERAL_ANIMATION_SPEED
                if self.frame_index < total - 1:
                    self.frame_index += 1
                self.image = self.assets["jump_frames"][
                    self.frame_index // GENERAL_ANIMATION_SPEED
                ]
            else:
                self.image = (
                    self.assets["static_left"]
                    if self.last_direction == "left"
                    else self.assets["static_right"]
                )

        elif self.animate:
            if self.moving_left and self.assets.get("left_frames"):
                self.frame_index = (self.frame_index + 1) % (
                    len(self.assets["left_frames"]) * GENERAL_ANIMATION_SPEED
                )
                self.image = self.assets["left_frames"][
                    self.frame_index // GENERAL_ANIMATION_SPEED
                ]

            elif not self.moving_left and self.assets.get("right_frames"):
                self.frame_index = (self.frame_index + 1) % (
                    len(self.assets["right_frames"]) * GENERAL_ANIMATION_SPEED
                )
                self.image = self.assets["right_frames"][
                    self.frame_index // GENERAL_ANIMATION_SPEED
                ]
            else:
                self.image = (
                    self.assets["static_left"]
                    if self.last_direction == "left"
                    else self.assets["static_right"]
                )

        else:
            self.frame_index = 0
            self.image = (
                self.assets["static_left"]
                if self.last_direction == "left"
                else self.assets["static_right"]
            )

    def draw(self, screen, camera_x):
        """
        Draw the player relative to the camera position.
        """
        y_offset = 10 if self.jumping else 0
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - y_offset))

    def get_mask(self):
        """
        Return a pixel-perfect collision mask for the current frame.
        """
        return pygame.mask.from_surface(self.image)