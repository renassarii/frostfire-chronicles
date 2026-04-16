import os

import pygame

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h

FPS = 60

WHITE = (180, 180, 255)
RED = (255, 0, 0)

SCALE_FACTOR = 5.5
GENERAL_ANIMATION_SPEED = 5
CROUCH_ANIMATION_SPEED = 1
UNCROUCH_ANIMATION_SPEED = 1

JUMP_HEIGHT = 120
FLOOR_Y = HEIGHT - 50

FIRE_SPEED = 4