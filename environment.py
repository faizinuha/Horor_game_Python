import pygame
import random
from asset_manager import AssetManager

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, wall_type="stone"):
        super().__init__()
        self.asset_manager = AssetManager()
        
        # Try to load wall sprite from assets
        if wall_type == "medieval_a":
            self.image = self.asset_manager.get_building_sprite("wall_a", 1)
        elif wall_type == "medieval_b":
            self.image = self.asset_manager.get_building_sprite("wall_b", 1)
        elif wall_type == "medieval_c":
            self.image = self.asset_manager.get_building_sprite("wall_c", 1)
        else:
            # Fallback to generated wall
            self.image = pygame.Surface([width, height])
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
        
        # Scale if needed
        if hasattr(self, 'image') and self.image.get_width() != width:
            self.image = pygame.transform.scale(self.image, (width, height))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, tree_type="oak"):
        super().__init__()
        self.asset_manager = AssetManager()
        
        # Try to load tree sprite from assets
        if tree_type == "medieval_1":
            self.image = self.asset_manager.get_environment_sprite("tree", 1)
        elif tree_type == "medieval_2":
            self.image = self.asset_manager.get_environment_sprite("tree", 2)
        else:
            # Fallback to generated tree
            self.image = pygame.Surface((64, 80))
            self.image.fill((0, 255, 0))
            self.image.set_colorkey((0, 255, 0))
            
            if tree_type == "oak":
                # Tree trunk
                pygame.draw.rect(self.image, (101, 67, 33), (28, 50, 8, 30))
                # Tree leaves
                pygame.draw.circle(self.image, (34, 139, 34), (32, 40), 25)
                pygame.draw.circle(self.image, (0, 100, 0), (32, 40), 22)
            elif tree_type == "pine":
                # Pine trunk
                pygame.draw.rect(self.image, (101, 67, 33), (30, 55, 4, 25))
                # Pine leaves (triangular)
                pygame.draw.polygon(self.image, (0, 100, 0), [(32, 15), (12, 45), (52, 45)])
                pygame.draw.polygon(self.image, (0, 100, 0), [(32, 25), (16, 55), (48, 55)])
        
        self.rect = self.image.get_rect(center=(x, y))

class House(pygame.sprite.Sprite):
    def __init__(self, x, y, house_type="village"):
        super().__init__()
        self.asset_manager = AssetManager()
        
        # Create house using building components
        self.image = pygame.Surface((120, 140))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 255, 0))
        
        # Try to use building assets
        wall_sprite = self.asset_manager.get_building_sprite("wall_a", 1)
        roof_sprite = self.asset_manager.get_building_sprite("roof_a", 1)
        door_sprite = self.asset_manager.get_building_sprite("door", 1)
        window_sprite = self.asset_manager.get_building_sprite("window", 1)
        
        if wall_sprite and wall_sprite.get_width() > 10:
            # Use asset-based house
            wall_scaled = pygame.transform.scale(wall_sprite, (100, 80))
            self.image.blit(wall_scaled, (10, 50))
            
            if roof_sprite:
                roof_scaled = pygame.transform.scale(roof_sprite, (120, 60))
                self.image.blit(roof_scaled, (0, 0))
            
            if door_sprite:
                door_scaled = pygame.transform.scale(door_sprite, (20, 40))
                self.image.blit(door_scaled, (50, 90))
            
            if window_sprite:
                window_scaled = pygame.transform.scale(window_sprite, (15, 15))
                self.image.blit(window_scaled, (25, 70))
                self.image.blit(window_scaled, (80, 70))
        else:
            # Fallback to generated house
            if house_type == "village":
                # House walls
                pygame.draw.rect(self.image, (139, 69, 19), (10, 50, 100, 90))
                # Roof
                pygame.draw.polygon(self.image, (178, 34, 34), [(5, 50), (60, 15), (115, 50)])
                # Door
                pygame.draw.rect(self.image, (101, 67, 33), (50, 100, 20, 40))
                # Windows
                pygame.draw.rect(self.image, (135, 206, 235), (25, 70, 15, 15))
                pygame.draw.rect(self.image, (135, 206, 235), (80, 70, 15, 15))
        
        self.rect = self.image.get_rect(center=(x, y))

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, rock_type=1):
        super().__init__()
        self.asset_manager = AssetManager()
        
        # Try to load rock sprite from assets
        self.image = self.asset_manager.get_environment_sprite("rock", rock_type)
        
        if not self.image or self.image.get_width() < 10:
            # Fallback to generated rock
            self.image = pygame.Surface((40, 30))
            self.image.fill((0, 255, 0))
            self.image.set_colorkey((0, 255, 0))
            pygame.draw.ellipse(self.image, (128, 128, 128), (0, 0, 40, 30))
            pygame.draw.ellipse(self.image, (100, 100, 100), (5, 5, 30, 20))
        
        self.rect = self.image.get_rect(center=(x, y))

class Barrel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.asset_manager = AssetManager()
        
        # Try to load barrel sprite from assets
        self.image = self.asset_manager.get_environment_sprite("barrel")
        
        if not self.image or self.image.get_width() < 10:
            # Fallback to generated barrel
            self.image = pygame.Surface((32, 40))
            self.image.fill((0, 255, 0))
            self.image.set_colorkey((0, 255, 0))
            pygame.draw.rect(self.image, (139, 69, 19), (4, 4, 24, 32))
            pygame.draw.ellipse(self.image, (101, 67, 33), (4, 2, 24, 8))
            pygame.draw.ellipse(self.image, (101, 67, 33), (4, 32, 24, 8))
        
        self.rect = self.image.get_rect(center=(x, y))

class Environment:
    def __init__(self):
        self.asset_manager = AssetManager()
        self.walls = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.current_area = "village"
        self.cave_entrance = None
        self.background_layers = []
        
        # Load background layers
        self.load_backgrounds()
        self._load_village()
        self._load_forest()
        self._load_cave()

    def load_backgrounds(self):
        """Load background layers from assets"""
        bg_layer_0 = self.asset_manager.get_background_sprite(0)
        bg_layer_1 = self.asset_manager.get_background_sprite(1)
        
        if bg_layer_0 and bg_layer_0.get_width() > 10:
            self.background_layers.append(bg_layer_0)
        if bg_layer_1 and bg_layer_1.get_width() > 10:
            self.background_layers.append(bg_layer_1)

    def _load_village(self):
        # Village boundaries using medieval walls
        self.walls.add(Wall(0, 0, 1600, 20, "medieval_a"))      # Top
        self.walls.add(Wall(0, 1180, 1600, 20, "medieval_a"))   # Bottom
        self.walls.add(Wall(0, 0, 20, 1200, "medieval_a"))      # Left
        self.walls.add(Wall(1580, 0, 20, 1200, "medieval_a"))   # Right
        
        # Village houses using asset-based houses
        house_positions = [
            (200, 200), (400, 180), (600, 220),
            (300, 400), (500, 450), (700, 400)
        ]
        
        for i, (x, y) in enumerate(house_positions):
            house = House(x, y, "village")
            self.decorations.add(house)
            # Add collision
            self.walls.add(Wall(house.rect.x + 10, house.rect.y + 40, 
                              house.rect.width - 20, house.rect.height - 40))
        
        # Trees using asset sprites
        tree_positions = [
            (100, 300), (150, 500), (700, 300), (750, 450),
            (800, 200), (900, 350), (1000, 250), (1100, 400)
        ]
        
        for i, (x, y) in enumerate(tree_positions):
            tree_type = "medieval_1" if i % 2 == 0 else "medieval_2"
            tree = Tree(x, y, tree_type)
            self.decorations.add(tree)
            # Add collision (smaller than visual)
            collision_rect = pygame.Rect(tree.rect.centerx - 20, tree.rect.centery - 15, 40, 30)
            collision_wall = Wall(collision_rect.x, collision_rect.y, 
                                collision_rect.width, collision_rect.height)
            self.walls.add(collision_wall)
        
        # Add barrels and crates using assets
        barrel_positions = [(250, 350), (450, 320), (650, 380)]
        for x, y in barrel_positions:
            barrel = Barrel(x, y)
            self.decorations.add(barrel)
            self.walls.add(Wall(barrel.rect.x, barrel.rect.y, 
                              barrel.rect.width, barrel.rect.height))
        
        # Add rocks using asset sprites
        rock_positions = [(800, 500), (850, 480), (900, 520), (950, 490)]
        for i, (x, y) in enumerate(rock_positions):
            rock = Rock(x, y, (i % 5) + 1)
            self.decorations.add(rock)
            self.walls.add(Wall(rock.rect.x, rock.rect.y, 
                              rock.rect.width, rock.rect.height))

    def _load_forest(self):
        # Dense forest with asset-based trees
        for i in range(25):
            tree_x = random.randint(1000, 1500)
            tree_y = random.randint(200, 500)
            tree_type = "medieval_1" if i % 2 == 0 else "medieval_2"
            tree = Tree(tree_x, tree_y, tree_type)
            self.decorations.add(tree)
            
            # Add collision
            collision_rect = pygame.Rect(tree.rect.centerx - 20, tree.rect.centery - 15, 40, 30)
            collision_wall = Wall(collision_rect.x, collision_rect.y, 
                                collision_rect.width, collision_rect.height)
            self.walls.add(collision_wall)
        
        # Cave entrance
        cave_entrance = pygame.sprite.Sprite()
        cave_entrance.image = pygame.Surface((100, 80))
        cave_entrance.image.fill((50, 50, 50))  # Dark cave entrance
        pygame.draw.ellipse(cave_entrance.image, (20, 20, 20), (10, 20, 80, 60))
        cave_entrance.rect = cave_entrance.image.get_rect(center=(1400, 100))
        self.decorations.add(cave_entrance)
        self.cave_entrance = cave_entrance
        
        # Forest boundaries
        self.walls.add(Wall(900, 0, 20, 600, "wood"))    # Forest entrance
        self.walls.add(Wall(1580, 0, 20, 600, "wood"))   # Forest boundary

    def _load_cave(self):
        # Cave rocks using asset sprites
        if self.current_area == "cave":
            # Cave boundaries
            self.walls.add(Wall(0, 0, 1600, 20, "stone"))      # Top
            self.walls.add(Wall(0, 580, 1600, 20, "stone"))    # Bottom
            self.walls.add(Wall(0, 0, 20, 600, "stone"))       # Left
            self.walls.add(Wall(1580, 0, 20, 600, "stone"))    # Right
            
            # Cave rocks using asset sprites
            for i in range(20):
                rock_x = random.randint(100, 1500)
                rock_y = random.randint(100, 500)
                rock_type = (i % 5) + 1
                rock = Rock(rock_x, rock_y, rock_type)
                self.decorations.add(rock)
                self.walls.add(Wall(rock.rect.x, rock.rect.y, 
                                  rock.rect.width, rock.rect.height))

    def get_current_walls(self):
        return self.walls

    def draw(self, screen, camera_x=0, camera_y=0):
        # Draw background layers first
        if self.background_layers:
            for i, bg_layer in enumerate(self.background_layers):
                # Parallax scrolling for background layers
                parallax_x = camera_x * (0.5 + i * 0.2)
                parallax_y = camera_y * (0.3 + i * 0.1)
                
                # Tile the background
                bg_width = bg_layer.get_width()
                bg_height = bg_layer.get_height()
                
                start_x = int(-parallax_x % bg_width) - bg_width
                start_y = int(-parallax_y % bg_height) - bg_height
                
                for x in range(start_x, screen.get_width() + bg_width, bg_width):
                    for y in range(start_y, screen.get_height() + bg_height, bg_height):
                        screen.blit(bg_layer, (x, y))
        else:
            # Fallback background colors
            if self.current_area == "cave":
                screen.fill((30, 30, 30))  # Dark cave background
            else:
                screen.fill((34, 139, 34))  # Grass background
            
        # Draw decorations
        for decoration in self.decorations:
            screen_x = decoration.rect.x - camera_x
            screen_y = decoration.rect.y - camera_y
            if -200 < screen_x < screen.get_width() + 200 and -200 < screen_y < screen.get_height() + 200:
                screen.blit(decoration.image, (screen_x, screen_y))
        
        # Draw visible boundary walls only
        for wall in self.walls:
            if hasattr(wall, 'image') and wall.image.get_width() > 50:  # Only draw boundary walls
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