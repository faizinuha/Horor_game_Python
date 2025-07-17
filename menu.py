
import pygame

class Menu:
    def __init__(self, screen, font, small_font, screen_width, screen_height):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        self.screen_width = screen_width
        self.screen_height = screen_height
<<<<<<< HEAD
        self.options = ["Start", "Controller", "Settings", "Exit"]
        self.selected_option_index = 0
=======
>>>>>>> 521db75eeebef683aef995afc4fd1073e78d107c

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Horror Game", True, (255, 255, 255))
<<<<<<< HEAD
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 150))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) # White
            if i == self.selected_option_index:
                color = (255, 255, 0) # Yellow for selected option
            
            option_text = self.small_font.render(option, True, color)
            self.screen.blit(option_text, (self.screen_width // 2 - option_text.get_width() // 2, 250 + i * 60))
        pygame.display.flip()

    def navigate(self, direction):
        self.selected_option_index += direction
        if self.selected_option_index < 0:
            self.selected_option_index = len(self.options) - 1
        elif self.selected_option_index >= len(self.options):
            self.selected_option_index = 0
        return self.options[self.selected_option_index]

    def get_selected_option(self):
        return self.options[self.selected_option_index]

=======
        start = self.small_font.render("Press SPACE to Start", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 250))
        self.screen.blit(start, (self.screen_width // 2 - start.get_width() // 2, 350))
        pygame.display.flip()

>>>>>>> 521db75eeebef683aef995afc4fd1073e78d107c

