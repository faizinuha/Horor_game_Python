
import pygame

class Visuals:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.light_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

    def draw_light(self, screen, player_pos, light_radius):
        self.light_surface.fill((0, 0, 0, 255)) # Start with a black, opaque surface
        pygame.draw.circle(self.light_surface, (0, 0, 0, 0), player_pos, light_radius) # Draw transparent circle
        screen.blit(self.light_surface, (0, 0))


