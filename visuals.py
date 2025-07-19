import pygame

import pygame
import random

class Visuals:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.overlay = pygame.Surface((width, height))
        self.overlay.set_alpha(100)
        
        # Particle system for effects
        self.particles = []

    def add_particle_effect(self, x, y, effect_type="sparkle"):
        """Add particle effects for various events"""
        if effect_type == "sparkle":
            for _ in range(10):
                particle = {
                    'x': x + pygame.random.randint(-10, 10),
                    'y': y + pygame.random.randint(-10, 10),
                    'vx': pygame.random.randint(-2, 2),
                    'vy': pygame.random.randint(-3, -1),
                    'life': 30,
                    'color': (255, 255, 100)
                }
                self.particles.append(particle)
        elif effect_type == "quest_complete":
            for _ in range(20):
                particle = {
                    'x': x + pygame.random.randint(-20, 20),
                    'y': y + pygame.random.randint(-20, 20),
                    'vx': pygame.random.randint(-3, 3),
                    'vy': pygame.random.randint(-4, -1),
                    'life': 60,
                    'color': (100, 255, 100)
                }
                self.particles.append(particle)

    def update_particles(self):
        """Update all particles"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.1  # Gravity
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw_particles(self, screen, camera_x=0, camera_y=0):
        """Draw all particles"""
        for particle in self.particles:
            screen_x = particle['x'] - camera_x
            screen_y = particle['y'] - camera_y
            
            if 0 <= screen_x <= self.width and 0 <= screen_y <= self.height:
                alpha = min(255, particle['life'] * 8)
                color = (*particle['color'], alpha)
                pygame.draw.circle(screen, particle['color'], (int(screen_x), int(screen_y)), 2)

    def draw_day_night_cycle(self, screen, time_of_day=0.5):
        """Draw enhanced day/night overlay (0.0 = night, 1.0 = day)"""
        # Calculate base darkness
        if time_of_day < 0.8:  # Not full day
            base_darkness = int((0.8 - time_of_day) * 200)
            
            # Dawn/Dusk colors
            if 0.2 <= time_of_day <= 0.3:  # Dawn
                self.overlay.fill((base_darkness//2, base_darkness//4, 0))  # Orange tint
            elif 0.7 <= time_of_day <= 0.8:  # Dusk
                self.overlay.fill((base_darkness//3, 0, base_darkness//4))  # Purple tint
            else:  # Night
                self.overlay.fill((0, 0, base_darkness//3))  # Blue tint
                
            # Adjust alpha based on time
            alpha = min(255, base_darkness + 55)
            self.overlay.set_alpha(alpha)
            screen.blit(self.overlay, (0, 0))
            
            # Add stars at night
            if time_of_day < 0.2 or time_of_day > 0.8:
                for _ in range(50):
                    star_x = random.randint(0, self.width)
                    star_y = random.randint(0, self.height)
                    star_size = random.randint(1, 2)
                    pygame.draw.circle(screen, (255, 255, 255), (star_x, star_y), star_size)

    def draw_weather_effect(self, screen, weather="clear"):
        """Draw weather effects"""
        if weather == "rain":
            for _ in range(50):
                x = pygame.random.randint(0, self.width)
                y = pygame.random.randint(0, self.height)
                pygame.draw.line(screen, (100, 100, 255), (x, y), (x - 2, y + 10), 1)
        elif weather == "snow":
            for _ in range(30):
                x = pygame.random.randint(0, self.width)
                y = pygame.random.randint(0, self.height)
                pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)

    def draw_ui_elements(self, screen, player_health=100, player_mana=50):
        """Draw UI elements like health bar"""
        # Health bar
        health_bar_rect = pygame.Rect(20, 20, 200, 20)
        pygame.draw.rect(screen, (100, 0, 0), health_bar_rect)
        health_fill = pygame.Rect(20, 20, int(200 * (player_health / 100)), 20)
        pygame.draw.rect(screen, (255, 0, 0), health_fill)
        pygame.draw.rect(screen, (255, 255, 255), health_bar_rect, 2)
        
        # Health text
        health_text = pygame.font.Font(None, 24).render(f"HP: {player_health}/100", True, (255, 255, 255))
        screen.blit(health_text, (25, 25))
        
        # Mana bar
        mana_bar_rect = pygame.Rect(20, 50, 200, 20)
        pygame.draw.rect(screen, (0, 0, 100), mana_bar_rect)
        mana_fill = pygame.Rect(20, 50, int(200 * (player_mana / 100)), 20)
        pygame.draw.rect(screen, (0, 0, 255), mana_fill)
        pygame.draw.rect(screen, (255, 255, 255), mana_bar_rect, 2)
        
        # Mana text
        mana_text = pygame.font.Font(None, 24).render(f"MP: {player_mana}/100", True, (255, 255, 255))
        screen.blit(mana_text, (25, 55))

    def draw_minimap(self, screen, player_pos, npcs_pos):
        """Draw a simple minimap"""
        minimap_rect = pygame.Rect(self.width - 150, 20, 120, 120)
        pygame.draw.rect(screen, (0, 0, 0, 128), minimap_rect)
        pygame.draw.rect(screen, (255, 255, 255), minimap_rect, 2)
        
        # Draw player on minimap
        player_map_x = minimap_rect.x + int((player_pos[0] / 1600) * 120)
        player_map_y = minimap_rect.y + int((player_pos[1] / 1200) * 120)
        pygame.draw.circle(screen, (0, 255, 0), (player_map_x, player_map_y), 3)
        
        # Draw NPCs on minimap
        for npc_pos in npcs_pos:
            npc_map_x = minimap_rect.x + int((npc_pos[0] / 1600) * 120)
            npc_map_y = minimap_rect.y + int((npc_pos[1] / 1200) * 120)
            pygame.draw.circle(screen, (255, 255, 0), (npc_map_x, npc_map_y), 2)