from game_obj import *
import pygame
import numpy as np
from pygame.math import Vector2
import math


class ObservationSpace:
    def __init__(self, player: Player, enemy: Enemy):
        # all the values have been restricted in the range [-1,1]

        self.player_vel = Vector2(player.vel.x / MAX_SPEED, player.vel.y / MAX_SPEED)
        self.enemy_vel = Vector2(enemy.vel.x / MAX_SPEED, enemy.vel.y / MAX_SPEED)

        dx = enemy.pos.x - player.pos.x
        dy = enemy.pos.y - player.pos.y

        angle_to_enemy = math.atan2(-dy, dx) - math.radians(player.angle)
        self.angle_sin = math.sin(angle_to_enemy)
        self.angle_cos = math.cos(angle_to_enemy)

        max_dist = math.hypot(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dist = min(math.hypot(dx, dy) / max_dist, 1.0)

        self.player_hp = player.hp / PLAYER_MAX_HP
        self.enemy_hp = enemy.hp / enemy.max_hp

    def as_array(self):
        return np.array(
            [
                self.player_vel.x,
                self.player_vel.y,
                self.enemy_vel.x,
                self.enemy_vel.y,
                self.angle_sin,
                self.angle_cos,
                self.dist,
                self.player_hp,
                self.enemy_hp,
            ],
            dtype=np.float32,
        )


# defining Actions
ACTION_NOOP = 0
ACTION_LEFT = 1
ACTION_RIGHT = 2
ACTION_THRUST = 3
ACTION_SHOOT = 4

NUM_ACTIONS = 5


def apply_action(action, player: Player):
    if action == ACTION_LEFT:
        player.angle += player.rotation_speed
    elif action == ACTION_RIGHT:
        player.angle -= player.rotation_speed
    elif action == ACTION_THRUST:
        player.vel += Vector2(0, -player.thrust_strength).rotate(-player.angle)
    elif action == ACTION_SHOOT:
        pass


class SpaceDuelEnv:
    def __init__(self, player: Player, enemy: Enemy) -> None:
        self.player = player
        self.enemy = enemy

        self.prev_player_hp = player.hp
        self.pre_enemy_hp = enemy.hp

    def reset(self):
        self.player.hp = PLAYER_MAX_HP
        self.player.pos = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.player.vel = Vector2()
        self.player.angle = 0

        self.enemy.hp = self.enemy.max_hp
        self.enemy.vel = Vector2()

        self.prev_player_hp = self.player.hp
        self.pre_enemy_hp = self.enemy.hp

        return ObservationSpace(self.player, self.enemy).as_array()

    def step(self, action: int):
        reward = 0.0
        done = False

        apply_action(action, self.player)

        self.player.physics_update()
        self.enemy.update(self.player)
        if self.enemy.hp < self.pre_enemy_hp:
            reward += 0.5
        if self.player.hp < self.prev_player_hp:
            reward -= 0.5

        if self.enemy.hp <= 0:
            done = True
            reward += 10

        if self.player.hp <= 0:
            done = True
            reward -= 10

        self.pre_enemy_hp = self.enemy.hp
        self.prev_player_hp = self.player.hp

        obs = ObservationSpace(self.player, self.enemy).as_array()

        return obs, reward, done
