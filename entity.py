

import pygame
import math

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill((255, 0, 0))  # Red square for now
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2

    def update(self, player_rect):
        # Simple AI: move towards the player
        dx, dy = player_rect.x - self.rect.x, player_rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.rect.x += self.speed * dx / dist
            self.rect.y += self.speed * dy / dist


