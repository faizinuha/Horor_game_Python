import pygame
import random

class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, decoration_type):
        super().__init__()
        self.decoration_type = decoration_type
        self.image = self._create_decoration()
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def _create_decoration(self):
        if self.decoration_type == "tree":
            return self._create_tree()
        elif self.decoration_type == "rock":
            return self._create_rock()
        elif self.decoration_type == "bush":
            return self._create_bush()
        elif self.decoration_type == "flower":
            return self._create_flower()
        return pygame.Surface((32, 32))
        
    def _create_tree(self):
        image = pygame.Surface((64, 96), pygame.SRCALPHA)
        
        # Trunk
        trunk_color = (101, 67, 33)
        pygame.draw.rect(image, trunk_color, (24, 48, 16, 48))
        
        # Leaves
        leaf_colors = [(34, 139, 34), (0, 100, 0), (46, 139, 87)]
        for i in range(30):
            x = random.randint(8, 56)
            y = random.randint(0, 52)
            size = random.randint(8, 16)
            color = random.choice(leaf_colors)
            pygame.draw.circle(image, color, (x, y), size)
            
        return image
        
    def _create_rock(self):
        image = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        # Base rock shape
        rock_color = (128, 128, 128)
        points = [(16, 4), (28, 16), (24, 28), (8, 28), (4, 16)]
        pygame.draw.polygon(image, rock_color, points)
        
        # Add details
        darker = (100, 100, 100)
        for _ in range(3):
            x = random.randint(8, 24)
            y = random.randint(8, 24)
            pygame.draw.circle(image, darker, (x, y), 2)
            
        return image
        
    def _create_bush(self):
        image = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        # Multiple circles for bush shape
        bush_color = (0, 100, 0)
        positions = [(16, 16), (12, 20), (20, 20), (16, 24)]
        for pos in positions:
            pygame.draw.circle(image, bush_color, pos, 8)
            
        return image
        
    def _create_flower(self):
        image = pygame.Surface((16, 16), pygame.SRCALPHA)
        
        # Random flower color
        flower_colors = [(255, 192, 203), (255, 0, 0), (255, 255, 0), (238, 130, 238)]
        color = random.choice(flower_colors)
        
        # Draw petals
        for angle in range(0, 360, 45):
            x = 8 + 4 * pygame.math.cos(pygame.math.radians(angle))
            y = 8 + 4 * pygame.math.sin(pygame.math.radians(angle))
            pygame.draw.circle(image, color, (int(x), int(y)), 2)
            
        # Center of flower
        pygame.draw.circle(image, (255, 255, 0), (8, 8), 2)
        
        return image
