import pygame

class Menu:
    def __init__(self, screen, font, small_font, screen_width, screen_height, audio_manager):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.audio_manager = audio_manager
        self.options = ["Start", "Load Game", "Controller", "Settings", "Exit"]
        self.selected_option_index = 0

    def draw_menu(self):
        # Gradient background
        for y in range(self.screen_height):
            color_value = int(20 + (y / self.screen_height) * 60)
            pygame.draw.line(self.screen, (color_value, color_value // 2, color_value + 20), 
                           (0, y), (self.screen_width, y))
        
        # Draw pixel art decorations
        self._draw_pixel_decorations()
        
        # Title with pixel effect
        title = self.font.render("PIXEL ADVENTURE", True, (255, 255, 100))
        title_shadow = self.font.render("PIXEL ADVENTURE", True, (100, 100, 0))
        
        title_x = self.screen_width // 2 - title.get_width() // 2
        self.screen.blit(title_shadow, (title_x + 3, 153))  # Shadow
        self.screen.blit(title, (title_x, 150))

        # Menu options
        for i, option in enumerate(self.options):
            color = (255, 255, 255)
            if i == self.selected_option_index:
                color = (255, 255, 100)  # Yellow for selected
                # Draw selection box
                option_text = self.small_font.render(option, True, color)
                box_rect = pygame.Rect(self.screen_width // 2 - option_text.get_width() // 2 - 20,
                                     250 + i * 60 - 5, option_text.get_width() + 40, 50)
                pygame.draw.rect(self.screen, (100, 100, 0), box_rect, 3)
            
            option_text = self.small_font.render(option, True, color)
            self.screen.blit(option_text, (self.screen_width // 2 - option_text.get_width() // 2, 250 + i * 60))
        
        # Instructions
        instruction = self.small_font.render("Use WASD/Arrow Keys to navigate, SPACE/ENTER to select", True, (200, 200, 200))
        self.screen.blit(instruction, (self.screen_width // 2 - instruction.get_width() // 2, 500))
        
        pygame.display.flip()

    def _draw_pixel_decorations(self):
        # Draw some pixel art decorations around the menu
        # Trees
        self._draw_pixel_tree(100, 400)
        self._draw_pixel_tree(700, 350)
        
        # Clouds
        self._draw_pixel_cloud(200, 100)
        self._draw_pixel_cloud(500, 80)
        
        # Grass
        for x in range(0, self.screen_width, 40):
            self._draw_pixel_grass(x, self.screen_height - 50)

    def _draw_pixel_tree(self, x, y):
        # Tree trunk
        pygame.draw.rect(self.screen, (101, 67, 33), (x, y, 8, 24))
        # Tree leaves
        pygame.draw.circle(self.screen, (34, 139, 34), (x + 4, y - 8), 16)

    def _draw_pixel_cloud(self, x, y):
        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 20)
        pygame.draw.circle(self.screen, (255, 255, 255), (x + 15, y), 25)
        pygame.draw.circle(self.screen, (255, 255, 255), (x + 30, y), 20)

    def _draw_pixel_grass(self, x, y):
        for i in range(5):
            grass_x = x + i * 8
            pygame.draw.line(self.screen, (34, 139, 34), (grass_x, y), (grass_x, y - 10), 2)

    def navigate(self, direction):
        self.audio_manager.play_sound("menu_select")
        self.selected_option_index += direction
        if self.selected_option_index < 0:
            self.selected_option_index = len(self.options) - 1
        elif self.selected_option_index >= len(self.options):
            self.selected_option_index = 0
        return self.options[self.selected_option_index]

    def get_selected_option(self):
        return self.options[self.selected_option_index]