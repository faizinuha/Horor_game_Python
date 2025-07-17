

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
        self.wall_list = pygame.sprite.Group()
        # Create a simple room
        # Top wall
        self.wall_list.add(Wall(50, 50, 700, 20))
        # Bottom wall
        self.wall_list.add(Wall(50, 550, 700, 20))
        # Left wall
        self.wall_list.add(Wall(50, 70, 20, 480))
        # Right wall
        self.wall_list.add(Wall(730, 70, 20, 480))

    def draw(self, screen):
        self.wall_list.draw(screen)


