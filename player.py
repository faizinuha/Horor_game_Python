import pygame
from asset_manager import AssetManager

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Initialize asset manager
        self.asset_manager = AssetManager()
        
        # Animation states
        self.current_action = "idle"
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10
        
        # Load initial sprite
        self.image = self.asset_manager.get_player_sprite("idle", 0)
        if not self.image:
            self.image = self._create_fallback_sprite()
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3
        self.original_x = x
        self.original_y = y
        self.walking = False
        self.direction = "down"
    
    def _create_fallback_sprite(self):
        """Create fallback pixel art if assets not found"""
        image = pygame.Surface((32, 48))
        image.fill((0, 255, 0))
        image.set_colorkey((0, 255, 0))
        
        # Draw pixel art character
        pygame.draw.rect(image, (255, 220, 177), (8, 0, 16, 16))  # Head
        pygame.draw.rect(image, (139, 69, 19), (6, 0, 20, 8))     # Hair
        pygame.draw.rect(image, (0, 0, 0), (10, 4, 2, 2))         # Eyes
        pygame.draw.rect(image, (0, 0, 0), (20, 4, 2, 2))
        pygame.draw.rect(image, (0, 100, 200), (6, 16, 20, 20))   # Shirt
        pygame.draw.rect(image, (139, 69, 19), (4, 36, 24, 12))   # Pants
        pygame.draw.rect(image, (255, 220, 177), (0, 18, 6, 16))  # Arms
        pygame.draw.rect(image, (255, 220, 177), (26, 18, 6, 16))
        
        return image

    def update(self, walls=None, dialogue_active=False):
        if dialogue_active:
            return  # Don't move during dialogue
            
        old_x, old_y = self.rect.x, self.rect.y
        dx, dy = 0, 0
        self.walking = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.walking = True
            self.direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.walking = True
            self.direction = "right"
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
            self.walking = True
            self.direction = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            self.walking = True
            self.direction = "down"
        
        # Update animation
        self._update_animation()

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
    
    def _update_animation(self):
        """Update player animation based on movement"""
        # Determine action
        if self.walking:
            action = "walk"
        else:
            action = "idle"
        
        # Update animation timer
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4  # 4 frames per animation
        
        # Load sprite if action changed
        if action != self.current_action:
            self.current_action = action
            self.animation_frame = 0
        
        # Get sprite from asset manager
        new_image = self.asset_manager.get_player_sprite(action, self.animation_frame)
        if new_image:
            self.image = new_image
        else:
            # Use fallback animation
            if self.walking and self.animation_timer == 0:
                self.rect.y += 1 if self.rect.y % 2 == 0 else -1


    def reset_position(self):
        self.rect.center = (self.original_x, self.original_y)