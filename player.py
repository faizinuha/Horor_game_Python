import pygame
from asset_manager import AssetManager

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.asset_manager = AssetManager()
        
        # Create pixel art player (16x24 pixels, scaled up)
        # Try to load sprite, fallback to generated art
        self.image = self.asset_manager.get_player_sprite("down", 0)
        if not self.image or self.image.get_width() == 32 and self.image.get_height() == 32:
            # Fallback to generated pixel art
            self.image = self.create_pixel_art_player()
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3
        self.original_x = x
        self.original_y = y
        
        # Animation variables
        self.animation_timer = 0
        self.walking = False
        self.direction = "down"
        self.animation_frame = 0
    
    def create_pixel_art_player(self):
        """Create pixel art player if no sprite found"""
        image = pygame.Surface((32, 48))
        image.fill((0, 255, 0))  # Transparent background
        image.set_colorkey((0, 255, 0))
        
        # Draw pixel art character
        # Head
        pygame.draw.rect(image, (255, 220, 177), (8, 0, 16, 16))  # Skin color
        pygame.draw.rect(image, (139, 69, 19), (6, 0, 20, 8))     # Hair
        pygame.draw.rect(image, (0, 0, 0), (10, 4, 2, 2))         # Left eye
        pygame.draw.rect(image, (0, 0, 0), (20, 4, 2, 2))         # Right eye
        pygame.draw.rect(image, (255, 0, 0), (14, 8, 4, 2))       # Mouth
        
        # Body
        pygame.draw.rect(image, (0, 100, 200), (6, 16, 20, 20))   # Blue shirt
        pygame.draw.rect(image, (139, 69, 19), (4, 36, 24, 12))   # Brown pants
        
        # Arms
        pygame.draw.rect(image, (255, 220, 177), (0, 18, 6, 16))  # Left arm
        pygame.draw.rect(image, (255, 220, 177), (26, 18, 6, 16)) # Right arm
        
        return image

    def update(self, walls=None):
        old_x, old_y = self.rect.x, self.rect.y
        dx, dy = 0, 0
        self.walking = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: 
            dx = -self.speed
            self.walking = True
            self.direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
            dx = self.speed
            self.walking = True
            self.direction = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]: 
            dy = -self.speed
            self.walking = True
            self.direction = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: 
            dy = self.speed
            self.walking = True
            self.direction = "down"

        # Move horizontally
        self.rect.x += dx
        if walls:
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dx > 0:
                        self.rect.right = wall.rect.left
                    elif dx < 0:
                        self.rect.left = wall.rect.right

        # Move vertically
        self.rect.y += dy
        if walls:
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dy > 0:
                        self.rect.bottom = wall.rect.top
                    elif dy < 0:
                        self.rect.top = wall.rect.bottom

        # Simple walking animation
        if self.walking:
            self.animation_timer += 1
            if self.animation_timer > 15:  # Change animation frame every 15 ticks
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 4
                
                # Try to load animated sprite
                new_image = self.asset_manager.get_player_sprite(self.direction, self.animation_frame)
                if new_image and new_image.get_width() > 32:  # Check if it's not placeholder
                    self.image = new_image

    def reset_position(self):
        self.rect.center = (self.original_x, self.original_y)