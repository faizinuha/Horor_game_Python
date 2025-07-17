
import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((100, 100, 100)) # Grey walls
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Environment:
    def __init__(self):
        self.levels = []
        self.current_level_index = 0
        self._load_levels()

    def _load_levels(self):
        # Level 1: Simple room
        level1_walls = pygame.sprite.Group()
        level1_walls.add(Wall(50, 50, 700, 20))  # Top
        level1_walls.add(Wall(50, 550, 700, 20)) # Bottom
        level1_walls.add(Wall(50, 70, 20, 480))  # Left
        level1_walls.add(Wall(730, 70, 20, 480)) # Right
        self.levels.append(level1_walls)

        # Level 2: Room with a central obstacle
        level2_walls = pygame.sprite.Group()
        level2_walls.add(Wall(50, 50, 700, 20))
        level2_walls.add(Wall(50, 550, 700, 20))
        level2_walls.add(Wall(50, 70, 20, 480))
        level2_walls.add(Wall(730, 70, 20, 480))
        level2_walls.add(Wall(200, 200, 400, 20)) # Obstacle
        level2_walls.add(Wall(200, 220, 20, 200)) # Obstacle
        level2_walls.add(Wall(580, 220, 20, 200)) # Obstacle
        level2_walls.add(Wall(200, 420, 400, 20)) # Obstacle
        self.levels.append(level2_walls)

    def get_current_walls(self):
        if self.current_level_index < len(self.levels):
            return self.levels[self.current_level_index]
        return pygame.sprite.Group() # Return empty group if no level

    def next_level(self):
        if self.current_level_index < len(self.levels) - 1:
            self.current_level_index += 1
            return True
        return False # No more levels

    def reset_levels(self):
        self.current_level_index = 0

    def draw(self, screen):
        self.get_current_walls().draw(screen)


