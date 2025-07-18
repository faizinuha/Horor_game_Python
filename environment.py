import pygame
import random

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
        elif wall_type == "invisible":
            self.image.fill((0, 255, 0))
            self.image.set_colorkey((0, 255, 0))  # Make invisible
        
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
            # Oak tree - brown trunk, green leaves
            pygame.draw.rect(self.image, (101, 67, 33), (20, 40, 8, 24))  # Trunk
            pygame.draw.circle(self.image, (34, 139, 34), (24, 32), 20)   # Leaves
            pygame.draw.circle(self.image, (0, 100, 0), (24, 32), 18, 2)  # Leaf outline
        else:  # Pine tree
            pygame.draw.rect(self.image, (101, 67, 33), (22, 45, 4, 19))  # Trunk
            pygame.draw.polygon(self.image, (0, 100, 0), [(24, 10), (8, 35), (40, 35)])  # Top
            pygame.draw.polygon(self.image, (0, 120, 0), [(24, 20), (12, 40), (36, 40)]) # Middle
            pygame.draw.polygon(self.image, (0, 140, 0), [(24, 30), (16, 45), (32, 45)]) # Bottom
        
        self.rect = self.image.get_rect(center=(x, y))

class House(pygame.sprite.Sprite):
    def __init__(self, x, y, house_type="village"):
        super().__init__()
        
        if house_type == "large":
            self.image = pygame.Surface((120, 140))
        else:
            self.image = pygame.Surface((80, 100))
            
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 255, 0))
        
        if house_type == "village":
            # Small village house
            pygame.draw.rect(self.image, (139, 69, 19), (10, 40, 60, 60))  # Walls
            pygame.draw.polygon(self.image, (178, 34, 34), [(5, 40), (40, 10), (75, 40)])  # Roof
            pygame.draw.rect(self.image, (101, 67, 33), (35, 70, 10, 30))  # Door
            pygame.draw.rect(self.image, (135, 206, 235), (20, 50, 8, 8))  # Window 1
            pygame.draw.rect(self.image, (135, 206, 235), (52, 50, 8, 8))  # Window 2
            pygame.draw.rect(self.image, (0, 0, 0), (20, 50, 8, 8), 1)     # Window frame 1
            pygame.draw.rect(self.image, (0, 0, 0), (52, 50, 8, 8), 1)     # Window frame 2
        elif house_type == "large":
            # Large house
            pygame.draw.rect(self.image, (160, 82, 45), (10, 50, 100, 90))  # Walls
            pygame.draw.polygon(self.image, (139, 69, 19), [(5, 50), (60, 15), (115, 50)])  # Roof
            pygame.draw.rect(self.image, (101, 67, 33), (50, 100, 20, 40))  # Door
            pygame.draw.rect(self.image, (135, 206, 235), (25, 70, 12, 12)) # Window 1
            pygame.draw.rect(self.image, (135, 206, 235), (83, 70, 12, 12)) # Window 2
            pygame.draw.rect(self.image, (135, 206, 235), (25, 100, 12, 12)) # Window 3
            pygame.draw.rect(self.image, (135, 206, 235), (83, 100, 12, 12)) # Window 4
            # Chimney
            pygame.draw.rect(self.image, (100, 50, 50), (80, 20, 12, 30))
        
        self.rect = self.image.get_rect(center=(x, y))

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, rock_type=1):
        super().__init__()
        size = random.randint(24, 40)
        self.image = pygame.Surface((size, size))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 255, 0))
        
        # Different rock colors and shapes
        colors = [(128, 128, 128), (100, 100, 100), (150, 150, 150), (80, 80, 80)]
        color = random.choice(colors)
        
        # Draw irregular rock shape
        points = []
        center_x, center_y = size // 2, size // 2
        for i in range(8):
            angle = i * 45
            radius = random.randint(size // 3, size // 2)
            x_point = center_x + radius * 0.7
            y_point = center_y + radius * 0.7
            points.append((x_point, y_point))
        
        pygame.draw.polygon(self.image, color, points)
        pygame.draw.polygon(self.image, (color[0] - 20, color[1] - 20, color[2] - 20), points, 2)
        
        self.rect = self.image.get_rect(center=(x, y))

class Barrel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 32))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 255, 0))
        
        # Barrel body
        pygame.draw.rect(self.image, (139, 69, 19), (2, 4, 20, 24))
        pygame.draw.ellipse(self.image, (101, 67, 33), (2, 2, 20, 8))  # Top
        pygame.draw.ellipse(self.image, (101, 67, 33), (2, 24, 20, 8)) # Bottom
        # Metal bands
        pygame.draw.rect(self.image, (128, 128, 128), (0, 8, 24, 2))
        pygame.draw.rect(self.image, (128, 128, 128), (0, 18, 24, 2))
        
        self.rect = self.image.get_rect(center=(x, y))

class Crate(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((28, 28))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 255, 0))
        
        # Crate body
        pygame.draw.rect(self.image, (139, 69, 19), (2, 2, 24, 24))
        pygame.draw.rect(self.image, (101, 67, 33), (2, 2, 24, 24), 2)
        # Wood planks
        pygame.draw.line(self.image, (160, 82, 45), (2, 8), (26, 8))
        pygame.draw.line(self.image, (160, 82, 45), (2, 14), (26, 14))
        pygame.draw.line(self.image, (160, 82, 45), (2, 20), (26, 20))
        pygame.draw.line(self.image, (160, 82, 45), (8, 2), (8, 26))
        pygame.draw.line(self.image, (160, 82, 45), (20, 2), (20, 26))
        
        self.rect = self.image.get_rect(center=(x, y))

class Environment:
    def __init__(self):
        self.walls = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.current_area = "village"
        self.cave_entrance = None
        self.world_width = 2000
        self.world_height = 1500
        self._load_village()
        self._load_forest()

    def _load_village(self):
        # Village boundaries (invisible walls)
        self.walls.add(Wall(0, 0, self.world_width, 20, "invisible"))      # Top
        self.walls.add(Wall(0, self.world_height-20, self.world_width, 20, "invisible"))   # Bottom
        self.walls.add(Wall(0, 0, 20, self.world_height, "invisible"))      # Left
        self.walls.add(Wall(self.world_width-20, 0, 20, self.world_height, "invisible"))   # Right
        
        # Village houses with collision
        house1 = House(200, 200, "village")
        house2 = House(400, 180, "village")
        house3 = House(600, 220, "village")
        house4 = House(300, 400, "large")
        house5 = House(500, 450, "village")
        house6 = House(700, 400, "large")
        house7 = House(150, 500, "village")
        house8 = House(800, 250, "large")
        
        self.decorations.add(house1, house2, house3, house4, house5, house6, house7, house8)
        
        # Add house collision walls
        for house in [house1, house2, house3, house4, house5, house6, house7, house8]:
            self.walls.add(Wall(house.rect.x, house.rect.y, house.rect.width, house.rect.height, "invisible"))
        
        # Trees around village
        trees = []
        for i in range(15):
            tree_x = random.randint(50, 900)
            tree_y = random.randint(100, 600)
            tree_type = random.choice(["oak", "pine"])
            
            # Avoid placing trees too close to houses
            too_close = False
            for house in [house1, house2, house3, house4, house5, house6, house7, house8]:
                if abs(tree_x - house.rect.centerx) < 100 and abs(tree_y - house.rect.centery) < 100:
                    too_close = True
                    break
            
            if not too_close:
                tree = Tree(tree_x, tree_y, tree_type)
                trees.append(tree)
                self.decorations.add(tree)
                # Add smaller collision for trees
                collision_rect = pygame.Rect(tree.rect.centerx - 15, tree.rect.centery - 10, 30, 20)
                self.walls.add(Wall(collision_rect.x, collision_rect.y, collision_rect.width, collision_rect.height, "invisible"))
        
        # Add environment objects
        # Barrels
        for i in range(5):
            barrel_x = random.randint(100, 800)
            barrel_y = random.randint(100, 500)
            barrel = Barrel(barrel_x, barrel_y)
            self.decorations.add(barrel)
            self.walls.add(Wall(barrel.rect.x, barrel.rect.y, barrel.rect.width, barrel.rect.height, "invisible"))
        
        # Crates
        for i in range(3):
            crate_x = random.randint(200, 700)
            crate_y = random.randint(200, 400)
            crate = Crate(crate_x, crate_y)
            self.decorations.add(crate)
            self.walls.add(Wall(crate.rect.x, crate.rect.y, crate.rect.width, crate.rect.height, "invisible"))

    def _load_forest(self):
        # Dense forest area
        for i in range(30):
            tree_x = random.randint(1000, 1800)
            tree_y = random.randint(100, 700)
            tree_type = random.choice(["oak", "pine"])
            tree = Tree(tree_x, tree_y, tree_type)
            self.decorations.add(tree)
            
            # Add tree collision
            collision_rect = pygame.Rect(tree.rect.centerx - 15, tree.rect.centery - 10, 30, 20)
            self.walls.add(Wall(collision_rect.x, collision_rect.y, collision_rect.width, collision_rect.height, "invisible"))
        
        # Forest rocks
        for i in range(15):
            rock_x = random.randint(1000, 1800)
            rock_y = random.randint(100, 700)
            rock = Rock(rock_x, rock_y)
            self.decorations.add(rock)
            self.walls.add(Wall(rock.rect.x, rock.rect.y, rock.rect.width, rock.rect.height, "invisible"))
        
        # Cave entrance
        cave_entrance = pygame.sprite.Sprite()
        cave_entrance.image = pygame.Surface((120, 100))
        cave_entrance.image.fill((0, 255, 0))
        cave_entrance.image.set_colorkey((0, 255, 0))
        
        # Draw cave entrance
        pygame.draw.ellipse(cave_entrance.image, (40, 40, 40), (10, 30, 100, 70))
        pygame.draw.ellipse(cave_entrance.image, (20, 20, 20), (20, 40, 80, 50))
        pygame.draw.rect(cave_entrance.image, (60, 60, 60), (0, 70, 120, 30))  # Ground
        
        cave_entrance.rect = cave_entrance.image.get_rect(center=(1400, 100))
        self.decorations.add(cave_entrance)
        self.cave_entrance = cave_entrance
    
    def load_cave_area(self):
        """Load cave-specific decorations and walls"""
        # Clear existing decorations for cave
        cave_decorations = pygame.sprite.Group()
        cave_walls = pygame.sprite.Group()
        
        # Cave boundaries
        cave_walls.add(Wall(0, 0, self.world_width, 20, "stone"))      # Top
        cave_walls.add(Wall(0, self.world_height-20, self.world_width, 20, "stone"))    # Bottom
        cave_walls.add(Wall(0, 0, 20, self.world_height, "stone"))       # Left
        cave_walls.add(Wall(self.world_width-20, 0, 20, self.world_height, "stone"))    # Right
        
        # Cave rocks and obstacles
        for i in range(25):
            rock_x = random.randint(100, self.world_width-100)
            rock_y = random.randint(100, self.world_height-100)
            rock = Rock(rock_x, rock_y)
            cave_decorations.add(rock)
            cave_walls.add(Wall(rock.rect.x, rock.rect.y, rock.rect.width, rock.rect.height, "invisible"))
        
        # Cave exit
        exit_marker = pygame.sprite.Sprite()
        exit_marker.image = pygame.Surface((60, 40))
        exit_marker.image.fill((100, 255, 100))
        pygame.draw.rect(exit_marker.image, (0, 255, 0), (10, 10, 40, 20))
        exit_marker.rect = exit_marker.image.get_rect(center=(100, 100))
        cave_decorations.add(exit_marker)
        
        return cave_decorations, cave_walls
    
    def load_village_decorations(self):
        """Load village-specific decorations"""
        # Village well
        well = pygame.sprite.Sprite()
        well.image = pygame.Surface((32, 32))
        well.image.fill((128, 128, 128))
        pygame.draw.circle(well.image, (64, 64, 64), (16, 16), 14)
        pygame.draw.circle(well.image, (0, 0, 139), (16, 16), 10)
        well.rect = well.image.get_rect(center=(400, 300))
        self.decorations.add(well)
        self.walls.add(Wall(well.rect.x, well.rect.y, well.rect.width, well.rect.height, "invisible"))
        
        # Fences
        for i in range(5):
            fence_x = 250 + i * 40
            fence = pygame.sprite.Sprite()
            fence.image = pygame.Surface((8, 32))
            fence.image.fill((101, 67, 33))
            fence.rect = fence.image.get_rect(center=(fence_x, 350))
            self.decorations.add(fence)
            self.walls.add(Wall(fence.rect.x, fence.rect.y, fence.rect.width, fence.rect.height, "invisible"))

    def get_current_walls(self):
        return self.walls

    def draw(self, screen, camera_x=0, camera_y=0):
        # Different background for different areas
        if self.current_area == "cave":
            screen.fill((30, 30, 30))  # Dark cave background
        else:
            screen.fill((34, 139, 34))  # Grass background
            
        # Draw decorations first (background)
        for decoration in self.decorations:
            screen_x = decoration.rect.x - camera_x
            screen_y = decoration.rect.y - camera_y
            if -200 < screen_x < screen.get_width() + 200 and -200 < screen_y < screen.get_height() + 200:
                screen.blit(decoration.image, (screen_x, screen_y))
        
        # Draw visible walls (only stone walls, not invisible ones)
        for wall in self.walls:
            if hasattr(wall, 'image') and wall.image.get_alpha() != 0:  # Only draw visible walls
                screen_x = wall.rect.x - camera_x
                screen_y = wall.rect.y - camera_y
                if -200 < screen_x < screen.get_width() + 200 and -200 < screen_y < screen.get_height() + 200:
                    screen.blit(wall.image, (screen_x, screen_y))

    def reset_levels(self):
        self.current_area = "village"
        self.walls.empty()
        self.decorations.empty()
        self._load_village()
        self._load_forest()