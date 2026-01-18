import pygame
import random
import math

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
GREEN = (60, 255, 60)
CYAN = (0, 255, 255)

MAX_SPEED = 8
BOUNDARY_PADDING = 20

PLAYER_MAX_HP = 200
ENEMY_BASE_HP = 100

PLAYER_DAMAGE = 25
ENEMY_DAMAGE = 15

TOTAL_LEVELS = 4

CURR_LEVEL = 1
# =====================
# BULLET
# =====================


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, owner):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (5, 5), 5)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)

        self.vel = pygame.math.Vector2(0, -18).rotate(-angle)

        self.owner = owner
        self.radius = 5

    def update(self):
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).colliderect(self.rect):
            self.kill()


# =====================
# SHIP BASE
# =====================


class Ship(pygame.sprite.Sprite):
    def __init__(self, pos, color, max_hp):
        pygame.sprite.Sprite.__init__(self)

        self.original_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, color, [(20, 0), (0, 40), (40, 40)])
        pygame.draw.polygon(self.original_image, WHITE, [(20, 0), (0, 40), (40, 40)], 2)

        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.vel: pygame.Vector2 = pygame.math.Vector2()

        self.angle = 0
        self.rotation_speed = 4
        self.thrust_strength = 0.5
        self.friction = 0.98

        self.last_shot = 0
        self.shoot_delay = 400
        self.radius = 20

        self.max_hp = max_hp
        self.hp = max_hp

    def physics_update(self):
        self.vel *= self.friction
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.pos += self.vel

        # Hard boundaries
        if self.pos.x < BOUNDARY_PADDING:
            self.pos.x = BOUNDARY_PADDING

            self.vel.x = 0
        elif self.pos.x > SCREEN_WIDTH - BOUNDARY_PADDING:
            self.pos.x = SCREEN_WIDTH - BOUNDARY_PADDING
            self.vel.x = 0

        if self.pos.y < BOUNDARY_PADDING:
            self.pos.y = BOUNDARY_PADDING
            self.vel.y = 0
        elif self.pos.y > SCREEN_HEIGHT - BOUNDARY_PADDING:
            self.pos.y = SCREEN_HEIGHT - BOUNDARY_PADDING
            self.vel.y = 0

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def shoot(self, all_sprites, bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.pos, self.angle, self)
            all_sprites.add(bullet)
            bullets.add(bullet)


# =====================
# PLAYER
# =====================


class Player(Ship):
    def __init__(self, pos):
        super().__init__(pos, GREEN, PLAYER_MAX_HP)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.angle += self.rotation_speed
        if keys[pygame.K_d]:
            self.angle -= self.rotation_speed

        if keys[pygame.K_w]:
            self.vel += pygame.math.Vector2(0, -self.thrust_strength).rotate(
                -self.angle
            )
        if keys[pygame.K_s]:
            self.vel += pygame.math.Vector2(0, self.thrust_strength * 0.6).rotate(
                -self.angle
            )

        self.physics_update()


# =====================
# ENEMY
# =====================


class Enemy(Ship):
    def __init__(self, pos, level):
        super().__init__(pos, RED, ENEMY_BASE_HP + level * 20)
        self.rotation_speed = 2 + level * 0.3
        self.thrust_strength = 0.3 + level * 0.05
        self.shoot_delay = max(400, 900 - level * 120)
        self.shoot_trigger = False

    def update(self, target):
        dx = target.pos.x - self.pos.x
        dy = target.pos.y - self.pos.y

        target_angle = math.degrees(math.atan2(-dy, dx)) - 90
        diff = (target_angle - self.angle + 180) % 360 - 180

        if abs(diff) > 3:
            self.angle += self.rotation_speed * (1 if diff > 0 else -1)

        dist = math.hypot(dx, dy)

        if dist > 350:
            self.vel += pygame.math.Vector2(0, -self.thrust_strength).rotate(
                -self.angle
            )

        self.shoot_trigger = dist < 500 and abs(diff) < 12 and random.random() < 0.05
        self.physics_update()


def draw_health_bar(surface, x, y, w, h, hp, max_hp, color):
    ratio = hp / max_hp
    pygame.draw.rect(surface, WHITE, (x - 2, y - 2, w + 4, h + 4), 1)
    pygame.draw.rect(surface, color, (x, y, w * ratio, h))


def draw_aim_line(surface, ship):
    direction = pygame.math.Vector2(0, -1).rotate(-ship.angle)
    pygame.draw.line(surface, CYAN, ship.pos, ship.pos + direction * 300, 2)
