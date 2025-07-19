import pygame
import random
import math

class WeatherSystem:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particles = []
        
        # Weather states
        self.current_weather = "clear"
        self.target_weather = "clear"
        self.transition_progress = 1.0
        self.transition_speed = 0.001
        
        # Weather effects
        self.wind_speed = 0
        self.wind_direction = 0
        self.lightning_timer = 0
        self.thunder_delay = 0
        
        # Particle properties
        self.weather_particles = {
            "rain": {
                "color": (200, 200, 255),
                "size": 2,
                "speed": 15,
                "count": 100,
                "angle": 70
            },
            "storm": {
                "color": (180, 180, 255),
                "size": 3,
                "speed": 25,
                "count": 200,
                "angle": 60
            },
            "snow": {
                "color": (255, 255, 255),
                "size": 2,
                "speed": 2,
                "count": 50,
                "angle": 90
            },
            "fog": {
                "color": (200, 200, 200),
                "size": 3,
                "speed": 1,
                "count": 300,
                "angle": 0
            }
        }

    def update(self, delta_time, time_of_day):
        # Update weather transition
        if self.transition_progress < 1.0:
            self.transition_progress += self.transition_speed * delta_time
            if self.transition_progress >= 1.0:
                self.current_weather = self.target_weather
        
        # Update wind
        self.wind_speed = self._get_wind_speed()
        self.wind_direction += math.sin(pygame.time.get_ticks() * 0.001) * 0.1
        
        # Update particles
        self._update_particles(delta_time)
        
        # Handle special weather effects
        if self.current_weather == "storm":
            self._handle_storm(delta_time)
            
    def _get_wind_speed(self):
        """Calculate wind speed based on weather"""
        base_speed = {
            "clear": 1,
            "cloudy": 2,
            "rain": 3,
            "storm": 5,
            "fog": 1,
            "snow": 1
        }.get(self.current_weather, 1)
        
        return base_speed * (1 + math.sin(pygame.time.get_ticks() * 0.001) * 0.5)
        
    def _update_particles(self, delta_time):
        """Update weather particles"""
        if self.current_weather in self.weather_particles:
            props = self.weather_particles[self.current_weather]
            
            # Add new particles
            while len(self.particles) < props["count"]:
                self.particles.append(self._create_particle(props))
            
            # Update existing particles
            for particle in self.particles[:]:
                particle["y"] += props["speed"] * delta_time * 60
                particle["x"] += self.wind_speed * delta_time * 60
                
                # Remove particles that are off screen
                if particle["y"] > self.screen_height or \
                   particle["x"] < 0 or particle["x"] > self.screen_width:
                    self.particles.remove(particle)
                    
    def _create_particle(self, props):
        """Create a new weather particle"""
        return {
            "x": random.randint(0, self.screen_width),
            "y": random.randint(-50, 0),
            "size": props["size"],
            "color": props["color"]
        }
        
    def _handle_storm(self, delta_time):
        """Handle storm effects including lightning"""
        self.lightning_timer -= delta_time
        if self.lightning_timer <= 0:
            if random.random() < 0.1:  # 10% chance of lightning
                self.lightning_timer = random.uniform(5, 15)
                self.thunder_delay = random.uniform(0.5, 2.0)
                return True
        return False
        
    def draw(self, screen):
        """Draw weather effects"""
        # Draw particles
        for particle in self.particles:
            pygame.draw.circle(screen, particle["color"],
                            (int(particle["x"]), int(particle["y"])),
                            particle["size"])
            
        # Draw fog
        if self.current_weather == "fog":
            fog_surface = pygame.Surface((self.screen_width, self.screen_height))
            fog_surface.fill((200, 200, 200))
            fog_surface.set_alpha(100)
            screen.blit(fog_surface, (0, 0))
            
        # Draw lightning flash
        if self.current_weather == "storm" and self.lightning_timer <= 0.1:
            flash_surface = pygame.Surface((self.screen_width, self.screen_height))
            flash_surface.fill((255, 255, 255))
            flash_surface.set_alpha(100)
            screen.blit(flash_surface, (0, 0))
            
    def change_weather(self, new_weather):
        """Change weather with transition"""
        if new_weather != self.current_weather:
            self.target_weather = new_weather
            self.transition_progress = 0.0
            self.particles = []  # Clear existing particles

class TimeSystem:
    def __init__(self):
        self.time = 0.5  # Start at noon (0.0 = midnight, 0.5 = noon, 1.0 = midnight)
        self.day = 1
        self.time_speed = 0.0001  # Time passing speed
        
        # Time periods
        self.periods = {
            "dawn": (0.2, 0.3),
            "morning": (0.3, 0.4),
            "noon": (0.4, 0.6),
            "afternoon": (0.6, 0.7),
            "dusk": (0.7, 0.8),
            "night": (0.8, 1.0)
        }
        
    def update(self, delta_time):
        """Update time of day"""
        self.time += self.time_speed * delta_time
        if self.time >= 1.0:
            self.time = 0.0
            self.day += 1
            
    def get_current_period(self):
        """Get current time period"""
        for period, (start, end) in self.periods.items():
            if start <= self.time < end or \
               (period == "night" and (self.time >= start or self.time < 0.2)):
                return period
        return "night"
        
    def get_light_level(self):
        """Get current light level (0.0 = dark, 1.0 = bright)"""
        period = self.get_current_period()
        if period == "noon":
            return 1.0
        elif period == "night":
            return 0.2
        elif period in ["dawn", "dusk"]:
            return 0.5
        else:
            return 0.8
