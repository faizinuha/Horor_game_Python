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
        elif house_type == "large":
            # Larger house
            pygame.draw.rect(self.image, (160, 82, 45), (5, 30, 70, 70))
            pygame.draw.polygon(self.image, (139, 69, 19), [(0, 30), (40, 5), (80, 30)])
            pygame.draw.rect(self.image, (101, 67, 33), (30, 70, 12, 30))
            pygame.draw.rect(self.image, (135, 206, 235), (15, 45, 10, 10))
            pygame.draw.rect(self.image, (135, 206, 235), (55, 45, 10, 10))
        
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
        
        # Village houses with collision
        house1 = House(200, 200, "village")
        house2 = House(400, 180, "village")
        house3 = House(600, 220, "village")
        house4 = House(300, 400, "large")
        house5 = House(500, 450, "village")
        house6 = House(700, 400, "large")
        
        self.decorations.add(house1, house2, house3, house4, house5, house6)
        
        # Add house collision walls
        self.walls.add(Wall(house1.rect.x, house1.rect.y, house1.rect.width, house1.rect.height))
        self.walls.add(Wall(house2.rect.x, house2.rect.y, house2.rect.width, house2.rect.height))
        self.walls.add(Wall(house3.rect.x, house3.rect.y, house3.rect.width, house3.rect.height))
        self.walls.add(Wall(house4.rect.x, house4.rect.y, house4.rect.width, house4.rect.height))
        self.walls.add(Wall(house5.rect.x, house5.rect.y, house5.rect.width, house5.rect.height))
        self.walls.add(Wall(house6.rect.x, house6.rect.y, house6.rect.width, house6.rect.height))
        
        # Trees around village with collision
        tree1 = Tree(100, 300, "oak")
        tree2 = Tree(150, 500, "oak")
        tree3 = Tree(700, 300, "pine")
        tree4 = Tree(750, 450, "pine")
        tree5 = Tree(800, 200, "oak")
        tree6 = Tree(900, 350, "oak")
        tree7 = Tree(1000, 250, "pine")
        tree8 = Tree(1100, 400, "oak")
        
        self.decorations.add(tree1, tree2, tree3, tree4, tree5, tree6, tree7, tree8)
        
        # Add tree collision (smaller than visual)
        for tree in [tree1, tree2, tree3, tree4, tree5, tree6, tree7, tree8]:
            collision_rect = pygame.Rect(tree.rect.centerx - 15, tree.rect.centery - 10, 30, 20)
            collision_wall = Wall(collision_rect.x, collision_rect.y, collision_rect.width, collision_rect.height)
            self.walls.add(collision_wall)
        
        # Forest area walls
        self.walls.add(Wall(50, 50, 200, 20, "wood"))   # Forest entrance
        self.walls.add(Wall(1200, 100, 20, 300, "wood"))  # Forest boundary
        
        # Village well (as decoration)
        well = pygame.sprite.Sprite()
        well.image = pygame.Surface((32, 32))
        well.image.fill((128, 128, 128))
        pygame.draw.circle(well.image, (64, 64, 64), (16, 16), 14)
        pygame.draw.circle(well.image, (0, 0, 139), (16, 16), 10)
        well.rect = well.image.get_rect(center=(400, 300))
        self.decorations.add(well)
        
        # Well collision
        self.walls.add(Wall(well.rect.x, well.rect.y, well.rect.width, well.rect.height))
        
        # Add more decorative elements
        # Fences
        for i in range(5):
            fence_x = 250 + i * 40
            fence = pygame.sprite.Sprite()
            fence.image = pygame.Surface((8, 32))
            fence.image.fill((101, 67, 33))
            fence.rect = fence.image.get_rect(center=(fence_x, 350))
            self.decorations.add(fence)
            self.walls.add(Wall(fence.rect.x, fence.rect.y, fence.rect.width, fence.rect.height))
        
        # Rocks
        for i in range(8):
            rock_x = 800 + i * 60
            rock_y = 500 + (i % 2) * 30
            rock = pygame.sprite.Sprite()
            rock.image = pygame.Surface((24, 16))
            rock.image.fill((128, 128, 128))
            pygame.draw.ellipse(rock.image, (100, 100, 100), (2, 2, 20, 12))
            rock.rect = rock.image.get_rect(center=(rock_x, rock_y))
            self.decorations.add(rock)
            self.walls.add(Wall(rock.rect.x, rock.rect.y, rock.rect.width, rock.rect.height))

    def get_current_walls(self):
        return self.walls

    def draw(self, screen, camera_x=0, camera_y=0):
        # Draw decorations first (background)
        for decoration in self.decorations:
            screen_x = decoration.rect.x - camera_x
            screen_y = decoration.rect.y - camera_y
            if -100 < screen_x < 900 and -100 < screen_y < 700:  # Only draw if on screen
                screen.blit(decoration.image, (screen_x, screen_y))
        
        # Draw visible walls only (boundaries)
        for wall in self.walls:
            if hasattr(wall, 'image') and wall.image.get_width() > 50:  # Only draw boundary walls
                screen_x = wall.rect.x - camera_x
                screen_y = wall.rect.y - camera_y
                if -100 < screen_x < 900 and -100 < screen_y < 700:
                    screen.blit(wall.image, (screen_x, screen_y))

    def reset_levels(self):
        self.current_area = "village"