import pygame
from asset_manager import AssetManager

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.asset_manager = AssetManager()
        
        # Load player sprite from assets
        self.image = self.asset_manager.get_player_sprite("idle")
        if not self.image or self.image.get_width() < 40:
            # Fallback to generated pixel art if asset not found
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
        self.current_action = "idle"
    
    def create_pixel_art_player(self):
        """Create pixel art player if no sprite found"""
        image = pygame.Surface((48, 64))
        image.fill((0, 255, 0))  # Transparent background
        image.set_colorkey((0, 255, 0))
        
        # Draw pixel art character (enhanced)
        # Head
        pygame.draw.rect(image, (255, 220, 177), (12, 4, 24, 20))  # Skin color
        pygame.draw.rect(image, (139, 69, 19), (8, 4, 32, 12))     # Hair
        pygame.draw.rect(image, (0, 0, 0), (16, 12, 3, 3))         # Left eye
        pygame.draw.rect(image, (0, 0, 0), (29, 12, 3, 3))         # Right eye
        pygame.draw.rect(image, (255, 100, 100), (20, 18, 8, 3))   # Mouth
        
        # Body
        pygame.draw.rect(image, (100, 150, 255), (8, 24, 32, 28))  # Blue shirt
        pygame.draw.rect(image, (139, 69, 19), (4, 52, 40, 12))    # Brown pants
        
        # Arms
        pygame.draw.rect(image, (255, 220, 177), (0, 28, 8, 20))   # Left arm
        pygame.draw.rect(image, (255, 220, 177), (40, 28, 8, 20))  # Right arm
        
        # Legs
        pygame.draw.rect(image, (139, 69, 19), (12, 52, 8, 12))    # Left leg
        pygame.draw.rect(image, (139, 69, 19), (28, 52, 8, 12))    # Right leg
        
        return image

    def update(self, walls=None, dialogue_active=False):
        # Don't move if dialogue is active
        if dialogue_active:
            self.walking = False
            return
            
        old_x, old_y = self.rect.x, self.rect.y
        dx, dy = 0, 0
        self.walking = False
        new_action = "idle"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: 
            dx = -self.speed
            self.walking = True
            self.direction = "left"
            new_action = "walk"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
            dx = self.speed
            self.walking = True
            self.direction = "right"
            new_action = "walk"
        if keys[pygame.K_UP] or keys[pygame.K_w]: 
            dy = -self.speed
            self.walking = True
            self.direction = "up"
            new_action = "walk"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: 
            dy = self.speed
            self.walking = True
            self.direction = "down"
            new_action = "walk"

        # Update sprite based on action
        if new_action != self.current_action:
            self.current_action = new_action
            new_image = self.asset_manager.get_player_sprite(new_action)
            if new_image and new_image.get_width() > 40:
                self.image = new_image

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

        # Animation for walking
        if self.walking:
            self.animation_timer += 1
            if self.animation_timer > 10:  # Change animation frame
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 4

    def reset_position(self):
        self.rect.center = (self.original_x, self.original_y)