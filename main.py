import os
import random
import sys

import pygame

from src.frostfire.assets import (
    load_environment_assets,
    load_fire_assets,
    load_ice_fire_assets,
    load_mountain_assets,
    load_player_assets,
)
from src.frostfire.characters.fire_npc import FireNPC
from src.frostfire.characters.ice_fire_npc import IceFireNPC
from src.frostfire.characters.player import Player
from src.frostfire.config import FLOOR_Y, FPS, HEIGHT, WHITE, WIDTH
from src.frostfire.levels.lvl1 import Level1

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frostfire Chronicles")


def game_over_menu(screen_surface):
    """
    Display a simple game over menu.

    Returns:
        str: "new_game" or "exit"
    """
    background = screen_surface.copy()

    menu_size = (int(WIDTH * 0.2), int(HEIGHT * 0.65))
    menu_image = pygame.transform.scale(
        pygame.image.load("assets/images/menu.png"), menu_size
    )
    menu_rect = menu_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    new_game_image = pygame.transform.scale(
        pygame.image.load("assets/images/new_game.png"), (200, 100)
    )
    exit_image = pygame.transform.scale(
        pygame.image.load("assets/images/exit.png"), (200, 100)
    )

    gap = 75
    new_game_rect = new_game_image.get_rect(
        center=(menu_rect.centerx, menu_rect.centery - gap)
    )
    exit_rect = exit_image.get_rect(
        center=(menu_rect.centerx, menu_rect.centery + gap)
    )

    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                if new_game_rect.collidepoint(mouse_position):
                    return "new_game"

                if exit_rect.collidepoint(mouse_position):
                    return "exit"

        screen_surface.blit(background, (0, 0))
        screen_surface.blit(menu_image, menu_rect)
        screen_surface.blit(new_game_image, new_game_rect)
        screen_surface.blit(exit_image, exit_rect)
        pygame.display.flip()


def create_npcs(level, player_assets):
    """
    Create a set of enemy NPCs across the level.
    """
    fire_assets = load_fire_assets(player_assets["size"])
    npc_list = []

    spawn_min = level.left_bound + 300
    spawn_max = level.right_bound - 300
    npc_count = 6
    spacing = (spawn_max - spawn_min) // (npc_count + 1)

    for index in range(npc_count):
        x_position = spawn_min + (index + 1) * spacing + random.randint(-30, 30)

        if random.random() < 0.5:
            npc = FireNPC(fire_assets)
        else:
            npc = IceFireNPC(load_ice_fire_assets(player_assets["size"]))

        npc.x = x_position
        npc.y = FLOOR_Y - npc.assets["fallback"].get_height()
        npc.speed = random.uniform(1.5, 4)
        npc.direction = random.choice([-1, 1])

        offset = random.randint(40, 100)
        npc.min_x = npc.x - offset
        npc.max_x = npc.x + offset

        npc_list.append(npc)

    return npc_list


def main_game():
    """
    Run the main gameplay loop.

    Returns:
        bool: True if the game ended because of game over.
    """
    player_assets = load_player_assets()
    environment_assets = load_environment_assets()
    mountain_assets = load_mountain_assets()

    level = Level1(mountain_assets)
    player = Player(player_assets)
    npcs = create_npcs(level, player_assets)

    clock = pygame.time.Clock()
    camera_x = 0
    game_over = False

    while True:
        clock.tick(FPS)
        screen.fill(WHITE)

        keys = pygame.key.get_pressed()
        previous_x = player.x

        player.update(keys)

        player.x = max(
            level.left_bound,
            min(player.x, level.right_bound - player.rect.width),
        )
        player.rect.x = int(player.x)

        for obstacle in level.obstacles:
            if player.rect.colliderect(obstacle):
                player.x = previous_x
                player.rect.x = int(previous_x)
                break

        if player.rect.x > WIDTH // 3:
            camera_x = player.rect.x - WIDTH // 3
        else:
            camera_x = 0

        level.draw(screen, camera_x)

        start_x = -(camera_x % 50)
        tile_count = (WIDTH // 50) + 2

        for index in range(tile_count):
            tile_x = start_x + index * 50
            tile_index = ((camera_x // 50) + index) % 4
            floor_key = f"floor{tile_index + 1}"
            screen.blit(environment_assets[floor_key], (tile_x, FLOOR_Y))

        for npc in npcs:
            npc.update((player.rect.x, player.rect.y))

            if isinstance(npc, FireNPC):
                offset = (int(npc.x - player.rect.x), int(npc.y - player.rect.y))
                if player.get_mask().overlap(npc.get_mask(), offset):
                    game_over = True
                    break

            elif isinstance(npc, IceFireNPC):
                if not npc.dead:
                    offset = (int(npc.x - player.rect.x), int(npc.y - player.rect.y))
                    if player.get_mask().overlap(npc.get_mask(), offset):
                        npc_height = npc.assets["fallback"].get_height()

                        if player.rect.bottom <= npc.y + npc_height * 0.8:
                            npc.kill()
                            player.y -= 20
                        else:
                            game_over = True
                            break

            if isinstance(npc, IceFireNPC):
                if not npc.finished:
                    npc.draw(screen, camera_x)
            else:
                npc.draw(screen, camera_x)

        if game_over:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.draw(screen, camera_x)
        pygame.display.flip()

    return game_over


def main():
    """
    Main entry point of the game.
    """
    while True:
        if main_game():
            selection = game_over_menu(screen)
            if selection == "exit":
                break
        else:
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()