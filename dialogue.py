import pygame

class DialogueBox:
    def __init__(self, screen, font, screen_width, screen_height):
        self.screen = screen
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.dialogues = []
        self.current_dialogue_index = 0
        self.visible = False
        self.box_rect = pygame.Rect(50, screen_height - 180, screen_width - 100, 120)
        self.text_color = (255, 255, 255)
        self.box_color = (20, 20, 40)
        self.border_color = (100, 100, 150)
        
        # Text animation
        self.text_speed = 2
        self.current_char_index = 0
        self.text_timer = 0
        self.full_text_displayed = False

    def set_dialogues(self, dialogues):
        self.dialogues = dialogues
        self.current_dialogue_index = 0
        self.current_char_index = 0
        self.full_text_displayed = False
        self.visible = True

    def next_dialogue(self):
        if not self.full_text_displayed:
            # If text is still animating, show full text immediately
            self.current_char_index = len(self.dialogues[self.current_dialogue_index])
            self.full_text_displayed = True
            return False
        
        if self.current_dialogue_index < len(self.dialogues) - 1:
            self.current_dialogue_index += 1
            self.current_char_index = 0
            self.full_text_displayed = False
        else:
            self.visible = False
            return True  # End of dialogue
        return False

    def update(self):
        if self.visible and not self.full_text_displayed:
            self.text_timer += 1
            if self.text_timer >= self.text_speed:
                self.text_timer = 0
                current_text = self.dialogues[self.current_dialogue_index]
                if self.current_char_index < len(current_text):
                    self.current_char_index += 1
                else:
                    self.full_text_displayed = True

    def draw(self):
        if self.visible and self.dialogues:
            # Draw dialogue box with pixel art style
            pygame.draw.rect(self.screen, self.box_color, self.box_rect)
            pygame.draw.rect(self.screen, self.border_color, self.box_rect, 4)
            
            # Draw inner border for pixel effect
            inner_rect = pygame.Rect(self.box_rect.x + 8, self.box_rect.y + 8, 
                                   self.box_rect.width - 16, self.box_rect.height - 16)
            pygame.draw.rect(self.screen, (40, 40, 80), inner_rect, 2)
            
            # Get current text (animated)
            current_text = self.dialogues[self.current_dialogue_index]
            displayed_text = current_text[:self.current_char_index]
            
            # Word wrap for long text
            words = displayed_text.split(' ')
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] < self.box_rect.width - 40:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line.strip())
            
            # Draw text lines
            for i, line in enumerate(lines[:3]):  # Max 3 lines
                text_surface = self.font.render(line, True, self.text_color)
                self.screen.blit(text_surface, (self.box_rect.x + 20, self.box_rect.y + 20 + i * 30))
            
            # Draw continue indicator
            if self.full_text_displayed:
                indicator_text = "Press SPACE to continue..."
                if self.current_dialogue_index >= len(self.dialogues) - 1:
                    indicator_text = "Press SPACE to close"
                
                indicator = pygame.font.Font(None, 24).render(indicator_text, True, (200, 200, 200))
                self.screen.blit(indicator, (self.box_rect.right - indicator.get_width() - 20, 
                                           self.box_rect.bottom - 25))
        
        # Update animation
        self.update()