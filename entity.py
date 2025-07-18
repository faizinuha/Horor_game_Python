import pygame
import random
import math
from asset_manager import AssetManager

class NPC(pygame.sprite.Sprite):
    def __init__(self, name, x, y, dialogues):
        super().__init__()
        self.asset_manager = AssetManager()
        self.name = name
        self.dialogues = dialogues
        self.original_x = x
        self.original_y = y
        self.wander_timer = 0
        self.wander_direction = random.choice([(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)])
        self.wander_speed = 0.5
        
        # Create enhanced pixel art NPC
        self.image = pygame.Surface((48, 64))
        self.image.fill((0, 255, 0))  # Transparent background
        self.image.set_colorkey((0, 255, 0))
        
        # Different colors for different NPCs
        colors = {
            "Elder": {"hair": (200, 200, 200), "shirt": (100, 50, 150), "pants": (50, 50, 50)},
            "Blacksmith": {"hair": (139, 69, 19), "shirt": (150, 75, 0), "pants": (101, 67, 33)},
            "Merchant": {"hair": (255, 215, 0), "shirt": (0, 150, 0), "pants": (139, 69, 19)},
            "Guide": {"hair": (139, 69, 19), "shirt": (34, 139, 34), "pants": (139, 69, 19)},
            "Villager": {"hair": (101, 67, 33), "shirt": (200, 100, 50), "pants": (50, 50, 100)},
            "Farmer": {"hair": (139, 69, 19), "shirt": (100, 150, 50), "pants": (101, 67, 33)},
            "Child": {"hair": (255, 215, 0), "shirt": (255, 100, 100), "pants": (0, 0, 200)},
            "Old Woman": {"hair": (150, 150, 150), "shirt": (100, 0, 100), "pants": (50, 50, 50)}
        }
        
        color = colors.get(name, {"hair": (139, 69, 19), "shirt": (200, 0, 0), "pants": (0, 0, 200)})
        
        # Draw pixel art NPC
        # Head
        pygame.draw.rect(self.image, (255, 220, 177), (12, 4, 24, 20))  # Skin
        pygame.draw.rect(self.image, color["hair"], (8, 4, 32, 12))     # Hair
        pygame.draw.rect(self.image, (0, 0, 0), (16, 12, 3, 3))        # Left eye
        pygame.draw.rect(self.image, (0, 0, 0), (29, 12, 3, 3))        # Right eye
        
        # Body
        pygame.draw.rect(self.image, color["shirt"], (8, 24, 32, 28))  # Shirt
        pygame.draw.rect(self.image, color["pants"], (4, 52, 40, 12))  # Pants
        
        # Arms
        pygame.draw.rect(self.image, (255, 220, 177), (0, 28, 8, 20))  # Left arm
        pygame.draw.rect(self.image, (255, 220, 177), (40, 28, 8, 20)) # Right arm
        
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        # Simple wandering behavior for some NPCs
        if self.name in ["Villager", "Child"]:
            self.wander_timer += 1
            
            if self.wander_timer > 120:  # Change direction every 2 seconds
                self.wander_direction = random.choice([(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)])
                self.wander_timer = 0
            
            # Move slightly
            new_x = self.rect.x + self.wander_direction[0] * self.wander_speed
            new_y = self.rect.y + self.wander_direction[1] * self.wander_speed
            
            # Keep within bounds of original position
            if abs(new_x - self.original_x) < 50 and abs(new_y - self.original_y) < 50:
                self.rect.x = new_x
                self.rect.y = new_y

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
            pygame.draw.rect(self.image, (255, 255, 0), (4, 4, 8, 2))  # Flower
        elif item_type == "coin":
            pygame.draw.circle(self.image, (255, 215, 0), (8, 8), 6)   # Gold coin
            pygame.draw.circle(self.image, (255, 255, 0), (8, 8), 4)   # Inner shine
        elif item_type == "potion":
            pygame.draw.rect(self.image, (100, 50, 150), (4, 2, 8, 12))  # Bottle
            pygame.draw.rect(self.image, (255, 0, 100), (5, 4, 6, 8))    # Liquid
            pygame.draw.rect(self.image, (101, 67, 33), (6, 1, 4, 3))    # Cork
        
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
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_x = x
        self.original_y = y
        
        # Create ghost sprite
        self.image = pygame.Surface((32, 48))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 255, 0))
        
        # Ghost body (semi-transparent white)
        pygame.draw.ellipse(self.image, (200, 200, 255), (4, 16, 24, 32))
        pygame.draw.circle(self.image, (200, 200, 255), (16, 16), 12)
        
        # Ghost eyes
        pygame.draw.circle(self.image, (0, 0, 0), (12, 12), 3)
        pygame.draw.circle(self.image, (0, 0, 0), (20, 12), 3)
        
        # Ghost mouth
        pygame.draw.ellipse(self.image, (0, 0, 0), (14, 18, 4, 6))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 1
        self.float_timer = 0
        self.chase_range = 150
        self.patrol_range = 100
        
    def update(self, player_pos):
        # Calculate distance to player
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Floating animation
        self.float_timer += 0.1
        float_offset = math.sin(self.float_timer) * 2
        
        if distance < self.chase_range:
            # Chase player
            if distance > 0:
                self.rect.x += (dx / distance) * self.speed
                self.rect.y += (dy / distance) * self.speed + float_offset
        else:
            # Patrol around original position
            patrol_dx = self.original_x - self.rect.centerx
            patrol_dy = self.original_y - self.rect.centery
            patrol_distance = math.sqrt(patrol_dx*patrol_dx + patrol_dy*patrol_dy)
            
            if patrol_distance > self.patrol_range:
                # Return to original position
                if patrol_distance > 0:
                    self.rect.x += (patrol_dx / patrol_distance) * (self.speed * 0.5)
                    self.rect.y += (patrol_dy / patrol_distance) * (self.speed * 0.5) + float_offset
            else:
                # Random movement within patrol range
                self.rect.x += random.randint(-1, 1)
                self.rect.y += random.randint(-1, 1) + float_offset