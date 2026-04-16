from pathlib import Path

import pygame
from PIL import Image, ImageSequence

from src.frostfire.config import SCALE_FACTOR

ASSETS_DIR = Path("assets")
IMAGES_DIR = ASSETS_DIR / "images"
GIFS_DIR = ASSETS_DIR / "gifs"


def load_gif_frames(gif_path, size):
    """
    Load all frames from a GIF file and scale them to the requested size.

    Returns an empty list if the file is missing.
    """
    gif_file = Path(gif_path)

    if not gif_file.exists():
        return []

    gif = Image.open(gif_file)
    frames = []

    for frame in ImageSequence.Iterator(gif):
        image = pygame.image.fromstring(
            frame.convert("RGBA").tobytes(),
            frame.size,
            "RGBA",
        )
        image = pygame.transform.scale(image, size)
        frames.append(image)

    return frames


def load_player_assets():
    """
    Load player sprites and animation frames.
    """
    static_right = pygame.image.load(IMAGES_DIR / "schneemann_right.png").convert_alpha()
    static_left = pygame.image.load(IMAGES_DIR / "schneemann_left.png").convert_alpha()

    original_width, original_height = static_right.get_size()
    new_size = (
        int(original_width * SCALE_FACTOR),
        int(original_height * SCALE_FACTOR),
    )

    static_right = pygame.transform.scale(static_right, new_size)
    static_left = pygame.transform.scale(static_left, new_size)

    right_frames = load_gif_frames(GIFS_DIR / "schneemann_right.gif", new_size)
    left_frames = load_gif_frames(GIFS_DIR / "schneemann_left.gif", new_size)
    jump_right_frames = load_gif_frames(GIFS_DIR / "jump_right.gif", new_size)
    jump_left_frames = load_gif_frames(GIFS_DIR / "jump_left.gif", new_size)
    jump_frames = load_gif_frames(GIFS_DIR / "jump.gif", new_size)

    crouch_left_frames = load_gif_frames(GIFS_DIR / "crouch_left.gif", new_size)
    uncrouch_left_frames = load_gif_frames(GIFS_DIR / "uncrouch_left.gif", new_size)
    crouch_right_frames = load_gif_frames(GIFS_DIR / "crouch_right.gif", new_size)
    uncrouch_right_frames = load_gif_frames(GIFS_DIR / "uncrouch_right.gif", new_size)

    crouched_left = pygame.image.load(IMAGES_DIR / "crouched_left.png").convert_alpha()
    crouched_right = pygame.image.load(IMAGES_DIR / "crouched_right.png").convert_alpha()

    crouched_left = pygame.transform.scale(crouched_left, new_size)
    crouched_right = pygame.transform.scale(crouched_right, new_size)

    return {
        "static_right": static_right,
        "static_left": static_left,
        "right_frames": right_frames,
        "left_frames": left_frames,
        "jump_right_frames": jump_right_frames,
        "jump_left_frames": jump_left_frames,
        "jump_frames": jump_frames,
        "crouch_left_frames": crouch_left_frames,
        "uncrouch_left_frames": uncrouch_left_frames,
        "crouched_left": crouched_left,
        "crouch_right_frames": crouch_right_frames,
        "uncrouch_right_frames": uncrouch_right_frames,
        "crouched_right": crouched_right,
        "size": new_size,
    }


def load_environment_assets():
    """
    Load floor tiles used for the ground.
    """
    floor1 = pygame.image.load(IMAGES_DIR / "floor1.png").convert_alpha()
    floor2 = pygame.image.load(IMAGES_DIR / "floor2.png").convert_alpha()
    floor3 = pygame.image.load(IMAGES_DIR / "floor3.png").convert_alpha()
    floor4 = pygame.image.load(IMAGES_DIR / "floor4.png").convert_alpha()

    floor1 = pygame.transform.scale(floor1, (50, 50))
    floor2 = pygame.transform.scale(floor2, (50, 50))
    floor3 = pygame.transform.scale(floor3, (50, 50))
    floor4 = pygame.transform.scale(floor4, (50, 50))

    return {
        "floor1": floor1,
        "floor2": floor2,
        "floor3": floor3,
        "floor4": floor4,
    }


def load_fire_assets(player_size):
    """
    Load animation frames for the fire enemy.
    """
    fire_size = (player_size[0] // 2, player_size[1] // 2)

    right_frames = load_gif_frames(GIFS_DIR / "fire_right.gif", fire_size)
    left_frames = load_gif_frames(GIFS_DIR / "fire_left.gif", fire_size)

    if not left_frames and right_frames:
        left_frames = [pygame.transform.flip(frame, True, False) for frame in right_frames]

    idle_frames = load_gif_frames(GIFS_DIR / "fire.gif", fire_size)

    fallback = pygame.Surface(fire_size, pygame.SRCALPHA)
    fallback.fill((255, 0, 0))

    return {
        "right_frames": right_frames,
        "left_frames": left_frames,
        "idle_frames": idle_frames,
        "fallback": fallback,
        "size": fire_size,
    }


def load_mountain_assets():
    """
    Load background and foreground mountain layers.
    """
    background_1 = pygame.image.load(IMAGES_DIR / "mountain_bg1.png").convert_alpha()
    background_2 = pygame.image.load(IMAGES_DIR / "mountain_bg2.png").convert_alpha()
    foreground = pygame.image.load(IMAGES_DIR / "mountain_fg.png").convert_alpha()

    return {
        "bg1": background_1,
        "bg2": background_2,
        "foreground": foreground,
    }


def load_ice_fire_assets(player_size):
    """
    Load animation frames for the ice-fire enemy.
    """
    enemy_size = (player_size[0] // 2, player_size[1] // 2)

    right_frames = load_gif_frames(GIFS_DIR / "ice_fire_right.gif", enemy_size)
    left_frames = load_gif_frames(GIFS_DIR / "ice_fire_left.gif", enemy_size)

    if not left_frames and right_frames:
        left_frames = [pygame.transform.flip(frame, True, False) for frame in right_frames]

    idle_frames = load_gif_frames(GIFS_DIR / "ice_fire.gif", enemy_size)
    dead_frames = load_gif_frames(GIFS_DIR / "dead_ice_fire.gif", enemy_size)

    fallback = pygame.Surface(enemy_size, pygame.SRCALPHA)
    fallback.fill((0, 191, 255))

    return {
        "right_frames": right_frames,
        "left_frames": left_frames,
        "idle_frames": idle_frames,
        "dead_frames": dead_frames,
        "fallback": fallback,
        "size": enemy_size,
    }