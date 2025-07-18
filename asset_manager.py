import pygame
import os

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.asset_path = "assets/"
        
        # Load all assets on initialization
        self.load_all_assets()
        
    def load_all_assets(self):
        """Load all available assets from the assets folder"""
        print("Loading assets...")
        
        # Load player sprites
        self.load_player_sprites()
        
        # Load environment assets
        self.load_environment_assets()
        
        # Load building assets
        self.load_building_assets()
        
        # Load background assets
        self.load_background_assets()
        
        print(f"Loaded {len(self.images)} assets successfully!")
    
    def load_image(self, filename, scale=None, colorkey=None):
        """Load and cache images"""
        if filename in self.images:
            return self.images[filename]
        
        try:
            full_path = os.path.join(self.asset_path, filename)
            if os.path.exists(full_path):
                image = pygame.image.load(full_path).convert_alpha()
                
                if colorkey:
                    image.set_colorkey(colorkey)
                
                if scale:
                    image = pygame.transform.scale(image, scale)
                
                self.images[filename] = image
                return image
        except Exception as e:
            print(f"Could not load image: {filename} - {e}")
        
        return self.create_placeholder_image()
    
    def create_placeholder_image(self, size=(32, 32), color=(255, 0, 255)):
        """Create placeholder image if asset not found"""
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface
    
    def load_player_sprites(self):
        """Load player animation sprites"""
        sprite_files = [
            "Sprite/Idle.png",
            "Sprite/Walk.png", 
            "Sprite/Run.png",
            "Sprite/Attack_1.png",
            "Sprite/Attack_2.png",
            "Sprite/Attack_3.png",
            "Sprite/Jump.png",
            "Sprite/Hurt.png",
            "Sprite/Dead.png",
            "Sprite/Shield.png"
        ]
        
        for sprite_file in sprite_files:
            self.load_image(sprite_file)
    
    def load_environment_assets(self):
        """Load environment assets"""
        env_files = [
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Tree 01.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Tree 02.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Rock 01.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Rock 02.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Rock 03.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Rock 04.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Rock 05.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Fence 01.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Fence 02.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Fence 03.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Barrel.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Storage.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Shop.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Quest Board.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Wooden Barrel.png",
            "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Wooden Crate.png"
        ]
        
        for env_file in env_files:
            self.load_image(env_file)
    
    def load_building_assets(self):
        """Load building assets"""
        building_files = [
            "Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Wall A 01.png",
            "Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Wall A 02.png",
            "Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Wall B 01.png",
            "Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Wall C 01.png",
            "Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Roof A 01.png",
            "Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Roof B 01.png",
            "Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Door 01.png",
            "Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Door 02.png",
            "Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Window 01.png",
            "Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Window 02.png"
        ]
        
        for building_file in building_files:
            self.load_image(building_file)
    
    def load_background_assets(self):
        """Load background assets"""
        bg_files = [
            "Background/Cartoon_Medieval_Guard_Post_2D_Level_Set_Background - Layer 00.png",
            "Background/Cartoon_Medieval_Guard_Post_2D_Level_Set_Background - Layer 01.png"
        ]
        
        for bg_file in bg_files:
            self.load_image(bg_file)
    
    def get_player_sprite(self, action="idle", frame=0):
        """Get player sprite based on action"""
        sprite_map = {
            "idle": "Sprite/Idle.png",
            "walk": "Sprite/Walk.png",
            "run": "Sprite/Run.png",
            "attack": "Sprite/Attack_1.png",
            "hurt": "Sprite/Hurt.png",
            "dead": "Sprite/Dead.png"
        }
        
        sprite_file = sprite_map.get(action, "Sprite/Idle.png")
        image = self.load_image(sprite_file, scale=(48, 64))
        return image
    
    def get_environment_sprite(self, env_type, variant=1):
        """Get environment sprite"""
        env_map = {
            "tree": f"Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Tree 0{variant}.png",
            "rock": f"Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Rock 0{variant}.png",
            "fence": f"Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Fence 0{variant}.png",
            "barrel": "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Barrel.png",
            "crate": "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Wooden Crate.png",
            "shop": "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Shop.png",
            "quest_board": "Environment/Cartoon_Medieval_Guard_Post_2D_Level_Set_Environment - Quest Board.png"
        }
        
        sprite_file = env_map.get(env_type, env_map["rock"])
        return self.load_image(sprite_file)
    
    def get_building_sprite(self, building_type, variant=1):
        """Get building sprite"""
        building_map = {
            "wall_a": f"Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Wall A 0{variant}.png",
            "wall_b": f"Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Wall B 0{variant}.png",
            "wall_c": f"Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Wall C 0{variant}.png",
            "roof_a": f"Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Roof A 0{variant}.png",
            "roof_b": f"Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Roof B 0{variant}.png",
            "door": f"Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Door 0{variant}.png",
            "window": f"Building/Cartoon_Medieval_Guard_Post_2D_Level_Set_Building - Window 0{variant}.png"
        }
        
        sprite_file = building_map.get(building_type, building_map["wall_a"])
        return self.load_image(sprite_file)
    
    def get_background_sprite(self, layer=0):
        """Get background sprite"""
        bg_file = f"Background/Cartoon_Medieval_Guard_Post_2D_Level_Set_Background - Layer 0{layer}.png"
        return self.load_image(bg_file)
    
    def get_platformer_sprite(self, ground_type=1):
        """Get platformer/ground sprite"""
        ground_file = f"Platformer/Cartoon_Medieval_Guard_Post_2D_Level_Set_Platformer - Ground {ground_type:02d}.png"
        return self.load_image(ground_file)