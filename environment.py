

import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((100, 100, 100)) # Grey walls
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Environment:
    def __init__(self):
        self.wall_list = [] # Tambah objek tembok di sini jika ada

    def draw(self, screen):
        # Tambah tembok jika ingin
        pass


