import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, wall_type="stone"):
        super().__init__()
        self.image = pygame.Surface([width, height])
        
        # Different wall types with pixel art patterns
        if wall_type == "stone":
            self.image.fill((128, 128, 128))
            # Add stone texture
            for i in range(0, width, 16):
                for j in range(0, height, 16):
                    pygame.draw.rect(self.image, (100, 100, 100), (i, j, 16, 16), 1)
        elif wall_type == "wood":
            self.image.fill((139, 69, 19))
            # Add wood grain
            for i in range(0, width, 8):
                pygame.draw.line(self.image, (101, 67, 33), (i, 0), (i, height))
        elif wall_type == "brick":
            self.image.fill((178, 34, 34))
            # Add brick pattern
            for i in range(0, width, 32):
                for j in range(0, height, 16):
                    offset = 16 if (j // 16) % 2 else 0
                    pygame.draw.rect(self.image, (139, 0, 0), (i + offset, j, 30, 14), 1)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, tree_type="oak"):
        super().__init__()
        self.image = pygame.Surface((48, 64))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 255, 0))
        
        if tree_type == "oak":
            # Tree trunk
            pygame.draw.rect(self.image, (101, 67, 33), (20, 40, 8, 24))
            # Tree leaves
            pygame.draw.circle(self.image, (34, 139, 34), (24, 32), 20)
            pygame.draw.circle(self.image, (0, 100, 0), (24, 32), 18)
        elif tree_type == "pine":
            # Pine trunk
            pygame.draw.rect(self.image, (101, 67, 33), (22, 45, 4, 19))
            # Pine leaves (triangular)
            pygame.draw.polygon(self.image, (0, 100, 0), [(24, 10), (8, 35), (40, 35)])
            pygame.draw.polygon(self.image, (0, 100, 0), [(24, 20), (12, 45), (36, 45)])
        
        self.rect = self.image.get_rect(center=(x, y))

class House(pygame.sprite.Sprite):
    def __init__(self, x, y, house_type="village"):
        super().__init__()
        self.image = pygame.Surface((80, 100))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 255, 0))
        
        if house_type == "village":
            # House walls
            pygame.draw.rect(self.image, (139, 69, 19), (10, 40, 60, 60))
            # Roof
            pygame.draw.polygon(self.image, (178, 34, 34), [(5, 40), (40, 10), (75, 40)])
            # Door
            pygame.draw.rect(self.image, (101, 67, 33), (35, 70, 10, 30))
            # Windows
            pygame.draw.rect(self.image, (135, 206, 235), (20, 50, 8, 8))
            pygame.draw.rect(self.image, (135, 206, 235), (52, 50, 8, 8))
        
        self.rect = self.image.get_rect(center=(x, y))

class Environment:
    def __init__(self):
        self.walls = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.current_area = "village"
        self._load_village()

    def _load_village(self):
        # Village boundaries
        self.walls.add(Wall(0, 0, 1600, 20, "stone"))      # Top
        self.walls.add(Wall(0, 1180, 1600, 20, "stone"))   # Bottom
        self.walls.add(Wall(0, 0, 20, 1200, "stone"))      # Left
        self.walls.add(Wall(1580, 0, 20, 1200, "stone"))   # Right
        
        # Village houses
        self.decorations.add(House(200, 200, "village"))
        self.decorations.add(House(400, 180, "village"))
        self.decorations.add(House(600, 220, "village"))
        self.decorations.add(House(300, 400, "village"))
        self.decorations.add(House(500, 450, "village"))
        
        # Trees around village
        self.decorations.add(Tree(100, 300, "oak"))
        self.decorations.add(Tree(150, 500, "oak"))
        self.decorations.add(Tree(700, 300, "pine"))
        self.decorations.add(Tree(750, 450, "pine"))
        self.decorations.add(Tree(800, 200, "oak"))
        
        # Village well (as decoration)
        well = pygame.sprite.Sprite()
        well.image = pygame.Surface((32, 32))
        well.image.fill((128, 128, 128))
        pygame.draw.circle(well.image, (64, 64, 64), (16, 16), 14)
        pygame.draw.circle(well.image, (0, 0, 139), (16, 16), 10)
        well.rect = well.image.get_rect(center=(400, 300))
        self.decorations.add(well)

    def get_current_walls(self):
        return self.walls

    def draw(self, screen, camera_x=0, camera_y=0):
        # Draw decorations first (background)
        for decoration in self.decorations:
            screen_x = decoration.rect.x - camera_x
            screen_y = decoration.rect.y - camera_y
            if -100 < screen_x < 900 and -100 < screen_y < 700:  # Only draw if on screen
                screen.blit(decoration.image, (screen_x, screen_y))
        
        # Draw walls
        for wall in self.walls:
            screen_x = wall.rect.x - camera_x
            screen_y = wall.rect.y - camera_y
            if -100 < screen_x < 900 and -100 < screen_y < 700:
                screen.blit(wall.image, (screen_x, screen_y))

    def reset_levels(self):
        self.current_area = "village"