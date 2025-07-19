import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Player stats
        self.max_health = 100
        self.health = self.max_health
        self.max_energy = 100
        self.energy = self.max_energy
        self.energy_regen = 0.5
        self.is_invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 1000  # 1 second of invulnerability after hit
        
        # Animation states
        self.current_action = "idle"
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10
        
        # Create initial sprite
        self.image = self._create_player_sprite("idle", 0)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3
        self.original_x = x
        self.original_y = y
        self.walking = False
        self.direction = "down"
        
        # Add stamina system
        self.stamina = 100
        self.max_stamina = 100
        self.stamina_regen = 0.5
        self.sprint_speed = 5
        self.sprint_drain = 1
        self.is_sprinting = False
    
    def _create_player_sprite(self, action, frame):
        """Create enhanced pixel art player sprite with advanced animations"""
        image = pygame.Surface((32, 48))
        image.fill((0, 255, 0))
        image.set_colorkey((0, 255, 0))
        
        # Base colors with shading
        skin_color = (255, 220, 177)
        skin_shadow = (230, 195, 152)
        hair_color = (139, 69, 19)
        hair_highlight = (169, 89, 39)
        shirt_color = (0, 100, 200)
        shirt_shadow = (0, 80, 160)
        pants_color = (139, 69, 19)
        pants_shadow = (119, 49, 0)
        
        if action == "walk":
            # Walking animation - slight bobbing
            y_offset = 1 if frame % 2 == 0 else 0
            
            # Head
            pygame.draw.rect(image, skin_color, (8, 0 + y_offset, 16, 16))
            pygame.draw.rect(image, hair_color, (6, 0 + y_offset, 20, 8))
            pygame.draw.rect(image, (0, 0, 0), (10, 4 + y_offset, 2, 2))  # Eyes
            pygame.draw.rect(image, (0, 0, 0), (20, 4 + y_offset, 2, 2))
            
            # Body
            pygame.draw.rect(image, shirt_color, (6, 16 + y_offset, 20, 20))
            pygame.draw.rect(image, pants_color, (4, 36 + y_offset, 24, 12))
            
            # Arms - animated
            arm_offset = 2 if frame % 2 == 0 else -2
            pygame.draw.rect(image, skin_color, (0, 18 + y_offset + arm_offset, 6, 16))
            pygame.draw.rect(image, skin_color, (26, 18 + y_offset - arm_offset, 6, 16))
            
            # Legs - walking animation
            leg_offset = 3 if frame % 2 == 0 else -3
            pygame.draw.rect(image, pants_color, (8, 44 + y_offset, 6, 4))  # Left leg
            pygame.draw.rect(image, pants_color, (18, 44 + y_offset, 6, 4)) # Right leg
            
        else:  # idle
            # Head
            pygame.draw.rect(image, skin_color, (8, 0, 16, 16))
            pygame.draw.rect(image, hair_color, (6, 0, 20, 8))
            pygame.draw.rect(image, (0, 0, 0), (10, 4, 2, 2))  # Eyes
            pygame.draw.rect(image, (0, 0, 0), (20, 4, 2, 2))
            
            # Body
            pygame.draw.rect(image, shirt_color, (6, 16, 20, 20))
            pygame.draw.rect(image, pants_color, (4, 36, 24, 12))
            
            # Arms
            pygame.draw.rect(image, skin_color, (0, 18, 6, 16))
            pygame.draw.rect(image, skin_color, (26, 18, 6, 16))
        
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
        
        # Load sprite if action changed or frame changed
        if action != self.current_action or self.animation_timer == 0:
            self.current_action = action
            self.image = self._create_player_sprite(action, self.animation_frame)

    def reset_position(self):
        self.rect.center = (self.original_x, self.original_y)
        
    def take_damage(self, amount):
        """Handle taking damage from monsters"""
        if not self.is_invulnerable:
            self.health = max(0, self.health - amount)
            self.is_invulnerable = True
            self.invulnerable_timer = pygame.time.get_ticks()
            return True
        return False
    
    def use_energy(self, amount):
        """Use energy for actions like sprinting"""
        if self.energy >= amount:
            self.energy = max(0, self.energy - amount)
            return True
        return False
    
    def update_stats(self, delta_time):
        """Update player stats like health and energy"""
        # Update invulnerability
        if self.is_invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerable_timer >= self.invulnerable_duration:
                self.is_invulnerable = False
        
        # Regenerate energy when not sprinting
        if not self.is_sprinting and self.energy < self.max_energy:
            self.energy = min(self.max_energy, self.energy + self.energy_regen * delta_time)
    
    def get_stats(self):
        """Get current player stats"""
        return {
            'health': self.health,
            'max_health': self.max_health,
            'energy': self.energy,
            'max_energy': self.max_energy
        }