import pygame
import time
from stable_baselines3 import DQN, dqn

from game_obj import *
from rl_env import SpaceDuelEnv
from space_duel_gym_env import SpaceDuelGymEnv

model = DQN.load("space_duel_dqn")

player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
enemy = Enemy((SCREEN_WIDTH * 0.75, SCREEN_HEIGHT / 2), level=1)


env = SpaceDuelEnv(player, enemy)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

obs = env.reset()
done = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    action, _ = model.predict(obs, deterministic=False)
    action = action.item()

    obs, reward, done = env.step(action)

    screen.fill(BLACK)

    draw_aim_line(screen, player)

    for bullet in env.player_bullets:
        screen.blit(bullet.image, bullet.rect)

    for bullet in env.enemy_bullets:
        screen.blit(bullet.image, bullet.rect)

    screen.blit(player.image, player.rect)
    screen.blit(enemy.image, enemy.rect)

    draw_health_bar(screen, 20, 20, 300, 15, player.hp, PLAYER_MAX_HP, GREEN)
    draw_health_bar(
        screen, SCREEN_WIDTH - 320, 20, 300, 15, enemy.hp, enemy.max_hp, RED
    )

    print(f"{env.player.pos}")
    print(f"{env.enemy.pos}")

    pygame.display.flip()
    clock.tick(60)

    if done:
        time.sleep(1)
        obs = env.reset()
        done = False
