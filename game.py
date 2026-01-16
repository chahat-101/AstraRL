import pygame
import random

class Entity:
    def __init__(self,pos):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0.0)
        self.alive = True
    
    def update(self,dt):
        pass
    
    def draw(self,screen):
        pass

    def is_alice(self):
        return self.alive


class Player(Entity):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("img/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 60))

        self.rect = self.image.get_rect(center=(400, 500))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed
    
    def draw(self,screen):
        screen.blit(self.image, self.rect)
    



class Enemy(Entity):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("img/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 60))

        self.rect = self.image.get_rect(center=(400, 500))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed
    
    def draw(self,screen):
        screen.blit(self.image, self.rect)
    





def main():
    pygame.init()

    WIDHT,HEIGHT = 800,600
    screen = pygame.display.set_mode((WIDHT,HEIGHT))
    pygame.display.set_caption("")