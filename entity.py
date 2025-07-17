import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, name, x, y, dialogues):
        super().__init__()
        self.name = name
        self.dialogues = dialogues
        
        # Create pixel art NPC
        self.image = pygame.Surface((32, 48))
        self.image.fill((0, 255, 0))  # Transparent background
        self.image.set_colorkey((0, 255, 0))
        
        # Different colors for different NPCs
        colors = {
            "Elder": {"hair": (200, 200, 200), "shirt": (100, 50, 150), "pants": (50, 50, 50)},
            "Blacksmith": {"hair": (139, 69, 19), "shirt": (150, 75, 0), "pants": (101, 67, 33)},
            "Merchant": {"hair": (255, 215, 0), "shirt": (0, 150, 0), "pants": (139, 69, 19)},
            "Guide": {"hair": (139, 69, 19), "shirt": (34, 139, 34), "pants": (139, 69, 19)}
        }
        
        color = colors.get(name, {"hair": (139, 69, 19), "shirt": (200, 0, 0), "pants": (0, 0, 200)})
        
        # Draw pixel art NPC
        # Head
        pygame.draw.rect(self.image, (255, 220, 177), (8, 0, 16, 16))  # Skin
        pygame.draw.rect(self.image, color["hair"], (6, 0, 20, 8))     # Hair
        pygame.draw.rect(self.image, (0, 0, 0), (10, 4, 2, 2))        # Left eye
        pygame.draw.rect(self.image, (0, 0, 0), (20, 4, 2, 2))        # Right eye
        
        # Body
        pygame.draw.rect(self.image, color["shirt"], (6, 16, 20, 20))  # Shirt
        pygame.draw.rect(self.image, color["pants"], (4, 36, 24, 12))  # Pants
        
        # Arms
        pygame.draw.rect(self.image, (255, 220, 177), (0, 18, 6, 16))  # Left arm
        pygame.draw.rect(self.image, (255, 220, 177), (26, 18, 6, 16)) # Right arm
        
        self.rect = self.image.get_rect(center=(x, y))

class QuestGiver(NPC):
    def __init__(self, name, x, y, dialogues, quest_id, quest_requirements):
        super().__init__(name, x, y, dialogues)
        self.quest_id = quest_id
        self.quest_name = f"Help the {name}"
        self.quest_description = "Complete the task given by " + name
        self.quest_requirements = quest_requirements
        
        # Add quest marker (yellow exclamation mark above head)
        pygame.draw.rect(self.image, (255, 255, 0), (14, -8, 4, 8))   # Exclamation mark
        pygame.draw.rect(self.image, (255, 255, 0), (15, -2, 2, 2))   # Dot

class Item(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        super().__init__()
        self.item_type = item_type
        
        # Create pixel art items
        self.image = pygame.Surface((16, 16))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 255, 0))
        
        if item_type == "herb":
            pygame.draw.rect(self.image, (0, 200, 0), (6, 8, 4, 8))    # Stem
            pygame.draw.rect(self.image, (0, 255, 0), (2, 2, 12, 6))   # Leaves
        elif item_type == "coin":
            pygame.draw.circle(self.image, (255, 215, 0), (8, 8), 6)   # Gold coin
            pygame.draw.circle(self.image, (255, 255, 0), (8, 8), 4)   # Inner shine
        
        self.rect = self.image.get_rect(center=(x, y))

class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, contents):
        super().__init__()
        self.contents = contents
        self.opened = False
        
        # Create pixel art chest
        self.image = pygame.Surface((32, 24))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 255, 0))
        
        # Chest body
        pygame.draw.rect(self.image, (139, 69, 19), (0, 8, 32, 16))    # Brown body
        pygame.draw.rect(self.image, (101, 67, 33), (0, 0, 32, 8))     # Lid
        pygame.draw.rect(self.image, (255, 215, 0), (14, 4, 4, 4))     # Lock
        
        self.rect = self.image.get_rect(center=(x, y))
    
    def open_chest(self):
        if not self.opened:
            self.opened = True
            # Redraw opened chest
            self.image.fill((0, 255, 0))
            pygame.draw.rect(self.image, (139, 69, 19), (0, 8, 32, 16))
            pygame.draw.rect(self.image, (101, 67, 33), (0, -4, 32, 8))  # Lid opened
            return self.contents
        return []