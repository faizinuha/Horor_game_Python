
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
        self.box_rect = pygame.Rect(50, screen_height - 150, screen_width - 100, 100)
        self.text_color = (255, 255, 255)
        self.box_color = (0, 0, 0, 180) # Semi-transparent black

    def set_dialogues(self, dialogues):
        self.dialogues = dialogues
        self.current_dialogue_index = 0
        self.visible = True

    def next_dialogue(self):
        if self.current_dialogue_index < len(self.dialogues) - 1:
            self.current_dialogue_index += 1
        else:
            self.visible = False
            return True # Indicates end of dialogue
        return False

    def draw(self):
        if self.visible and self.dialogues:
            pygame.draw.rect(self.screen, self.box_color, self.box_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.box_rect, 2) # Border

            text_surface = self.font.render(self.dialogues[self.current_dialogue_index], True, self.text_color)
            self.screen.blit(text_surface, (self.box_rect.x + 10, self.box_rect.y + 10))


