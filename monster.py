import pygame
import random
import math
from sprite_animation import CharacterSprite

class Monster(CharacterSprite):
    def __init__(self, x, y, monster_type, sprite_sheet_path="assets/Sprite/monster_sheet.png"):
        super().__init__(x, y, sprite_sheet_path, 48, 48)  # Monsters are slightly larger
        self.monster_type = monster_type
        self.health = 100
        self.damage = 20
        self.speed = 2
        self.detection_radius = 150
        self.attack_radius = 30
        self.state = "idle"
        self.attack_cooldown = 1000  # milliseconds
        self.last_attack = 0
        self.stunned = False
        self.stun_timer = 0
        
        # Different monster types
        if monster_type == "ghost":
            self.health = 80
            self.damage = 15
            self.speed = 3
            self.detection_radius = 200
            self.can_phase = True
        elif monster_type == "zombie":
            self.health = 120
            self.damage = 25
            self.speed = 1
            self.detection_radius = 100
        elif monster_type == "demon":
            self.health = 150
            self.damage = 35
            self.speed = 2.5
            self.detection_radius = 180
            self.can_teleport = True
            
    def update(self, delta_time, player_pos):
        if self.stunned:
            self.stun_timer -= delta_time
            if self.stun_timer <= 0:
                self.stunned = False
            return
            
        dx = player_pos[0] - self.rect.x
        dy = player_pos[1] - self.rect.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # State machine for monster behavior
        if distance <= self.attack_radius:
            self.state = "attack"
        elif distance <= self.detection_radius:
            self.state = "chase"
        else:
            self.state = "idle"
            
        # Update position and animation based on state
        if self.state == "chase":
            # Normalize direction
            if distance > 0:
                dx = dx / distance
                dy = dy / distance
                
            # Update position
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            
            # Set direction for animation
            if abs(dx) > abs(dy):
                self.direction = "right" if dx > 0 else "left"
            else:
                self.direction = "down" if dy > 0 else "up"
                
        # Special abilities based on monster type
        if self.monster_type == "ghost" and self.can_phase and random.random() < 0.01:
            self.phase_through_wall()
        elif self.monster_type == "demon" and self.can_teleport and random.random() < 0.005:
            self.teleport()
            
        super().update(delta_time)
        
    def take_damage(self, amount):
        self.health -= amount
        self.stunned = True
        self.stun_timer = 500  # Stun for 500ms
        return self.health <= 0
        
    def phase_through_wall(self):
        # Ghost can temporarily phase through walls
        self.can_phase = False
        pygame.time.set_timer(pygame.USEREVENT + 1, 5000)  # Reset phase ability after 5 seconds
        
    def teleport(self):
        # Demon can teleport short distances
        self.rect.x += random.randint(-100, 100)
        self.rect.y += random.randint(-100, 100)
        self.can_teleport = False
        pygame.time.set_timer(pygame.USEREVENT + 2, 10000)  # Reset teleport ability after 10 seconds

class MonsterSpawner:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_points = []
        self.monsters = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_interval = 10000  # 10 seconds between spawns
        self.max_monsters = 5
        
    def add_spawn_point(self, x, y):
        self.spawn_points.append((x, y))
        
    def update(self, delta_time, player_pos):
        self.spawn_timer += delta_time
        
        # Try to spawn new monster
        if self.spawn_timer >= self.spawn_interval and len(self.monsters) < self.max_monsters:
            self.spawn_timer = 0
            if self.spawn_points:
                spawn_point = random.choice(self.spawn_points)
                monster_type = random.choice(["ghost", "zombie", "demon"])
                new_monster = Monster(spawn_point[0], spawn_point[1], monster_type)
                self.monsters.add(new_monster)
                
        # Update all monsters
        for monster in self.monsters:
            monster.update(delta_time, player_pos)
            
    def draw(self, screen, camera_offset=(0, 0)):
        for monster in self.monsters:
            screen_pos = (monster.rect.x - camera_offset[0], 
                         monster.rect.y - camera_offset[1])
            screen.blit(monster.image, screen_pos)
