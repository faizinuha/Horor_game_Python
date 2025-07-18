import pygame
import os

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.asset_path = "assets/"
        
        # Create asset directories if they don't exist
        self.create_directories()
        
    def create_directories(self):
        """Create asset directories"""
        directories = [
            "assets/",
            "assets/sprites/",
            "assets/sprites/player/",
            "assets/sprites/npcs/",
            "assets/sprites/items/",
            "assets/sprites/environment/",
            "assets/sounds/",
            "assets/music/",
            "assets/fonts/"
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")
    
    def load_image(self, filename, scale=None, colorkey=None):
        """Load and cache images"""
        if filename in self.images:
            return self.images[filename]
        
        try:
            full_path = os.path.join(self.asset_path, filename)
            image = pygame.image.load(full_path)
            
            if colorkey:
                image.set_colorkey(colorkey)
            
            if scale:
                image = pygame.transform.scale(image, scale)
            
            self.images[filename] = image
            return image
        except:
            print(f"Could not load image: {filename}")
            return self.create_placeholder_image()
    
    def create_placeholder_image(self, size=(32, 32), color=(255, 0, 255)):
        """Create placeholder image if asset not found"""
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface
    
    def load_sound(self, filename):
        """Load and cache sounds"""
        if filename in self.sounds:
            return self.sounds[filename]
        
        try:
            full_path = os.path.join(self.asset_path, filename)
            sound = pygame.mixer.Sound(full_path)
            self.sounds[filename] = sound
            return sound
        except:
            print(f"Could not load sound: {filename}")
            return None
    
    def get_player_sprite(self, direction="down", frame=0):
        """Get player sprite based on direction and animation frame"""
        sprite_name = f"sprites/player/player_{direction}_{frame}.png"
        return self.load_image(sprite_name, scale=(32, 48))
    
    def get_npc_sprite(self, npc_name):
        """Get NPC sprite"""
        sprite_name = f"sprites/npcs/{npc_name.lower()}.png"
        return self.load_image(sprite_name, scale=(32, 48))
    
    def get_item_sprite(self, item_name):
        """Get item sprite"""
        sprite_name = f"sprites/items/{item_name}.png"
        return self.load_image(sprite_name, scale=(16, 16))
    
    def get_environment_sprite(self, env_name):
        """Get environment sprite"""
        sprite_name = f"sprites/environment/{env_name}.png"
        return self.load_image(sprite_name)
    
    def get_tileset(self, tileset_name):
        """Load tileset for environment"""
        sprite_name = f"sprites/environment/{tileset_name}.png"
        return self.load_image(sprite_name)