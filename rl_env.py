from game_obj import *
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


class SpaceDuelEnv:
    def __init__(self, player: Player, enemy: Enemy) -> None:
        self.player = player
        self.enemy = enemy

        self.prev_player_hp = player.hp
        self.pre_enemy_hp = enemy.hp

        self.player_bullets = []
        self.enemy_bullets = []
        self.player_shoot_cooldown = 0.0
        self.enemy_shoot_cooldown = 0.0

    def reset(self):
        self.player.hp = PLAYER_MAX_HP
        self.player.pos = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.player.vel = Vector2()
        self.player.angle = 0

        # max hp
        self.enemy.hp = self.enemy.max_hp
        self.enemy.vel = Vector2()
        self.prev_player_hp = self.player.hp
        self.pre_enemy_hp = self.enemy.hp

        # clearing shoot colldown
        self.player_shoot_cooldown = 0
        self.enemy_shoot_cooldown = 0

        # clearing bullets
        self.player_bullets.clear()
        self.enemy_bullets.clear()

        return ObservationSpace(self.player, self.enemy).as_array()

    def step(self, action: int):
        reward = 0.0
        done = False

        if action == ACTION_SHOOT:
            reward -= 0.01

        apply_action(action, self.player, self)

        self.player.physics_update()
        self.enemy.update(self.player)

        if self.player_shoot_cooldown > 0:
            self.player_shoot_cooldown -= 1

        new_player_bullets = []

        for bullet in self.player_bullets:
            bullet.update()

            distance = math.hypot(
                bullet.pos.x - self.enemy.pos.x, bullet.pos.y - self.enemy.pos.y
            )

            if distance < self.enemy.radius + bullet.radius:
                self.enemy.hp -= PLAYER_DAMAGE
                reward += 0.2
                continue

            if 0 < bullet.pos.x < SCREEN_WIDTH and 0 < bullet.pos.y < SCREEN_HEIGHT:
                new_player_bullets.append(bullet)

        self.player_bullets = new_player_bullets

        if self.enemy_shoot_cooldown > 0:
            self.enemy_shoot_cooldown -= 1

        if self.enemy_shoot_cooldown <= 0 and random.random() < 0.03:
            bullet = Bullet(self.enemy.pos, self.enemy.angle, owner=self.enemy)
            self.enemy_bullets.append(bullet)
            self.enemy_shoot_cooldown = 20

        new_enemy_bullets = []

        for bullet in self.enemy_bullets:
            bullet.update()

            if (
                math.hypot(
                    bullet.pos.x - self.player.pos.x, bullet.pos.y - self.player.pos.y
                )
                < self.player.radius + bullet.radius
            ):
                self.player.hp -= ENEMY_DAMAGE
                reward -= 0.5
                continue

            if 0 < bullet.pos.x < SCREEN_WIDTH and 0 < bullet.pos.y < SCREEN_HEIGHT:
                new_enemy_bullets.append(bullet)

        self.enemy_bullets = new_enemy_bullets

        if self.enemy.hp < self.pre_enemy_hp:
            reward += 0.5
        if self.player.hp < self.prev_player_hp:
            reward -= 0.5

        if self.enemy.hp <= 0:
            done = True
            reward += 5

        if self.player.hp <= 0:
            done = True
            reward -= 10

        self.pre_enemy_hp = self.enemy.hp
        self.prev_player_hp = self.player.hp

        obs = ObservationSpace(self.player, self.enemy).as_array()
        reward += (1.0 - obs[6]) * 0.005

        return obs, reward, done


def apply_action(action, player: Player, env: SpaceDuelEnv):
    if action == ACTION_LEFT:
        player.angle += player.rotation_speed
    elif action == ACTION_RIGHT:
        player.angle -= player.rotation_speed
    elif action == ACTION_THRUST:
        player.vel += Vector2(0, -player.thrust_strength).rotate(-player.angle)
    elif action == ACTION_SHOOT:
        if env.player_shoot_cooldown <= 0:
            bullet = Bullet(player.pos, player.angle, owner=player)
            env.player_bullets.append(bullet)

            env.player_shoot_cooldown = 15
