import pygame

class PauseMenu:
    def __init__(self, screen, font, small_font, screen_width, screen_height, audio_manager):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.audio_manager = audio_manager
        self.options = ["Resume", "Save Game", "Load Game", "Settings", "Main Menu"]
        self.selected_option_index = 0
        self.from_pause = False

    def draw_pause_menu(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Pause menu background
        menu_rect = pygame.Rect(200, 150, 400, 300)
        pygame.draw.rect(self.screen, (40, 40, 60), menu_rect)
        pygame.draw.rect(self.screen, (100, 100, 150), menu_rect, 4)
        
        # Title
        title = self.font.render("PAUSED", True, (255, 255, 255))
        title_x = self.screen_width // 2 - title.get_width() // 2
        self.screen.blit(title, (title_x, 180))

        # Menu options
        for i, option in enumerate(self.options):
            color = (255, 255, 255)
            if i == self.selected_option_index:
                color = (255, 255, 100)  # Yellow for selected
                # Draw selection box
                option_text = self.small_font.render(option, True, color)
                box_rect = pygame.Rect(self.screen_width // 2 - option_text.get_width() // 2 - 20,
                                     240 + i * 40 - 5, option_text.get_width() + 40, 35)
                pygame.draw.rect(self.screen, (100, 100, 0), box_rect, 2)
            
            option_text = self.small_font.render(option, True, color)
            self.screen.blit(option_text, (self.screen_width // 2 - option_text.get_width() // 2, 240 + i * 40))
        
        # Instructions
        instruction = self.small_font.render("Use WASD/Arrow Keys, SPACE/ENTER to select, ESC to resume", True, (200, 200, 200))
        self.screen.blit(instruction, (self.screen_width // 2 - instruction.get_width() // 2, 480))
        
        pygame.display.flip()

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