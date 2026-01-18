import pygame
import math
import random
import numpy as np
from pygame.math import Vector2

from game_obj import *

# =====================
# CONFIG
# =====================

# =====================
# RL
# =====================


# =====================
# UI
# =====================


# =====================
# GAME LOOP
# =====================


def main():
    global CURR_LEVEL
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Duel – Accurate Shooting")
    clock = pygame.time.Clock()

    player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    while CURR_LEVEL <= TOTAL_LEVELS:
        enemy = Enemy((SCREEN_WIDTH * 0.75, SCREEN_HEIGHT / 2), CURR_LEVEL)
        bullets = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group(player, enemy)  # type: ignore[arg-type]

        while enemy.hp > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.shoot(all_sprites, bullets)

            player.update()
            enemy.update(player)

            if enemy.shoot_trigger:
                enemy.shoot(all_sprites, bullets)
                enemy.shoot_trigger = False

            bullets.update()

            for bullet in bullets.copy():
                if bullet.owner == player and pygame.sprite.collide_circle(
                    bullet, enemy
                ):
                    enemy.hp -= PLAYER_DAMAGE
                    bullet.kill()
                elif bullet.owner == enemy and pygame.sprite.collide_circle(
                    bullet, player
                ):
                    player.hp -= ENEMY_DAMAGE
                    bullet.kill()

                    if player.hp <= 0:
                        player.hp = PLAYER_MAX_HP
                        player.pos = pygame.math.Vector2(
                            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
                        )
                        player.vel = pygame.math.Vector2()

            screen.fill(BLACK)
            draw_aim_line(screen, player)
            all_sprites.draw(screen)

            draw_health_bar(screen, 20, 20, 300, 15, player.hp, PLAYER_MAX_HP, GREEN)
            draw_health_bar(
                screen, SCREEN_WIDTH - 320, 20, 300, 15, enemy.hp, enemy.max_hp, RED
            )

            pygame.display.flip()
            clock.tick(FPS)

        CURR_LEVEL += 1

    pygame.quit()


if __name__ == "__main__":
    main()
