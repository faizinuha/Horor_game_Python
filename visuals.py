import pygame
class Visuals:
    def __init__(self, width, height):
        self.overlay = pygame.Surface((width, height))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(200)

    def draw_light(self, screen, center, radius):
        self.overlay.fill((0, 0, 0))
        pygame.draw.circle(self.overlay, (0, 0, 0, 0), center, radius)
        screen.blit(self.overlay, (0, 0))
