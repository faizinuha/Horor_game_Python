

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


class Ghost:
    def __init__(self):
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 0, 0))  # warna merah untuk si hantu
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 100
        self.direction = 1

    def update(self, player_rect):
        # Hantu ngikutin pemain secara sederhana
        if player_rect.x < self.rect.x:
            self.rect.x -= 1
        elif player_rect.x > self.rect.x:
            self.rect.x += 1

        if player_rect.y < self.rect.y:
            self.rect.y -= 1
        elif player_rect.y > self.rect.y:
            self.rect.y += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
