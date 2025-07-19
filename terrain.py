import pygame
import random
import math

class TerrainGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.noise_scale = 50
        self.water_level = 0.3
        self.mountain_level = 0.7

    def generate_height_map(self):
        """Generate a height map using Perlin noise"""
        height_map = [[0 for x in range(self.width)] for y in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                # Simplified noise generation (you might want to use a proper Perlin noise library)
                nx = x / self.width - 0.5
                ny = y / self.height - 0.5
                height_map[y][x] = self._noise(nx * self.noise_scale, ny * self.noise_scale)
        return height_map

    def _noise(self, x, y):
        """Simple noise function (placeholder for Perlin noise)"""
        n = x * 12.9898 + y * 78.233
        return (math.sin(n) * 43758.5453123) % 1.0

    def generate_terrain_features(self, height_map):
        """Generate terrain features based on height map"""
        features = []
        for y in range(self.height):
            for x in range(self.width):
                height = height_map[y][x]
                world_x = x * 32
                world_y = y * 32

                if height < self.water_level:
                    # Water bodies
                    features.append(('water', (world_x, world_y)))
                elif height > self.mountain_level:
                    # Mountains
                    features.append(('mountain', (world_x, world_y)))
                elif height > self.mountain_level - 0.1:
                    # Hills
                    features.append(('hill', (world_x, world_y)))
                else:
                    # Random vegetation
                    if random.random() < 0.1:
                        if random.random() < 0.7:
                            features.append(('tree', (world_x, world_y)))
                        else:
                            features.append(('rock', (world_x, world_y)))
        return features

class WaterBody:
    def __init__(self, x, y, width, height, water_type="river"):
        self.rect = pygame.Rect(x, y, width, height)
        self.water_type = water_type
        self.ripple_time = 0
        self.ripples = []
        
        # Water properties
        self.base_color = (0, 100, 255) if water_type == "river" else (0, 50, 200)
        self.transparency = 180
        self.flow_speed = 1 if water_type == "river" else 0.2
        
    def update(self, delta_time):
        # Update ripples
        self.ripple_time += delta_time
        if self.ripple_time > 0.5:  # Create new ripple every 0.5 seconds
            self.ripple_time = 0
            if len(self.ripples) < 10:
                x = random.randint(self.rect.left, self.rect.right)
                y = random.randint(self.rect.top, self.rect.bottom)
                self.ripples.append({'pos': (x, y), 'size': 1, 'alpha': 255})
        
        # Update existing ripples
        for ripple in self.ripples[:]:
            ripple['size'] += delta_time * 10
            ripple['alpha'] -= delta_time * 100
            if ripple['alpha'] <= 0:
                self.ripples.remove(ripple)

    def draw(self, screen, camera_offset=(0, 0)):
        # Draw base water
        water_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(water_surface, (*self.base_color, self.transparency), 
                        (0, 0, self.rect.width, self.rect.height))
        
        # Draw ripples
        for ripple in self.ripples:
            pygame.draw.circle(water_surface, (*self.base_color, int(ripple['alpha'])),
                             (ripple['pos'][0] - self.rect.x, ripple['pos'][1] - self.rect.y),
                             ripple['size'], 1)
        
        screen.blit(water_surface, 
                   (self.rect.x - camera_offset[0], 
                    self.rect.y - camera_offset[1]))

class Mountain:
    def __init__(self, x, y, size="large"):
        self.rect = pygame.Rect(x, y, 128 if size == "large" else 64, 
                              160 if size == "large" else 80)
        self.size = size
        self.snow_line = 0.7  # Percentage of height where snow begins
        
    def draw(self, screen, camera_offset=(0, 0)):
        # Draw mountain base
        points = self._get_mountain_points()
        adjusted_points = [(x - camera_offset[0], y - camera_offset[1]) for x, y in points]
        
        # Draw mountain body
        pygame.draw.polygon(screen, (100, 100, 100), adjusted_points)
        
        # Draw snow cap
        snow_points = self._get_snow_points(points)
        if snow_points:
            adjusted_snow_points = [(x - camera_offset[0], y - camera_offset[1]) 
                                  for x, y in snow_points]
            pygame.draw.polygon(screen, (255, 255, 255), adjusted_snow_points)
            
        # Add some detail lines
        self._draw_detail_lines(screen, adjusted_points, camera_offset)
        
    def _get_mountain_points(self):
        """Calculate mountain polygon points"""
        if self.size == "large":
            return [
                (self.rect.centerx - 60, self.rect.bottom),
                (self.rect.centerx - 40, self.rect.centery - 20),
                (self.rect.centerx, self.rect.top),
                (self.rect.centerx + 40, self.rect.centery - 20),
                (self.rect.centerx + 60, self.rect.bottom)
            ]
        else:
            return [
                (self.rect.centerx - 30, self.rect.bottom),
                (self.rect.centerx - 20, self.rect.centery - 10),
                (self.rect.centerx, self.rect.top),
                (self.rect.centerx + 20, self.rect.centery - 10),
                (self.rect.centerx + 30, self.rect.bottom)
            ]
            
    def _get_snow_points(self, mountain_points):
        """Calculate snow cap polygon points"""
        snow_height = self.rect.height * (1 - self.snow_line)
        snow_y = self.rect.top + snow_height
        return [p for p in mountain_points if p[1] <= snow_y]
        
    def _draw_detail_lines(self, screen, points, camera_offset):
        """Draw detail lines on the mountain"""
        center_x = points[2][0]
        center_y = points[2][1]
        
        for i in range(3):
            y_offset = self.rect.height * (0.3 + i * 0.2)
            left_x = center_x - self.rect.width * (0.3 - i * 0.1)
            right_x = center_x + self.rect.width * (0.3 - i * 0.1)
            y = center_y + y_offset
            
            pygame.draw.line(screen, (80, 80, 80),
                           (left_x, y),
                           (right_x, y), 2)
