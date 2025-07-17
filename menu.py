
import pygame

class Menu:
    def __init__(self, screen, font, small_font, screen_width, screen_height):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Horror Game", True, (255, 255, 255))
        start = self.small_font.render("Press SPACE to Start", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 250))
        self.screen.blit(start, (self.screen_width // 2 - start.get_width() // 2, 350))
        pygame.display.flip()


