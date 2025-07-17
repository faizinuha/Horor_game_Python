
import pygame
class Door(pygame.sprite.Sprite):
    def __init__(self, name, x, y, correct=False):
        super().__init__()
        self.name = name
        self.correct = correct
        self.image = pygame.Surface((80, 100))
        self.image.fill((100, 255, 100) if correct else (255, 100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1

    def update(self, player_rect):
        if self.rect.x < player_rect.x:
            self.rect.x += 1
        elif self.rect.x > player_rect.x:
            self.rect.x -= 1

    def reset_position(self):
        self.rect.x, self.rect.y = 100, 100

