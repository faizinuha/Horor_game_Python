import pygame
import os

def create_default_sprite_sheet(filename, width, height, rows, cols, color=(255, 255, 255)):
    """Create a default sprite sheet for development"""
    surface = pygame.Surface((width * cols, height * rows))
    surface.fill((0, 255, 0))  # Fill with transparency color
    
    for row in range(rows):
        for col in range(cols):
            # Draw a basic character shape
            sprite = pygame.Surface((width, height))
            sprite.fill((0, 255, 0))
            
            # Body
            pygame.draw.rect(sprite, color, (width//4, height//4, width//2, height//2))
            
            # Head
            pygame.draw.circle(sprite, color, (width//2, height//4), width//6)
            
            # Add to sheet
            surface.blit(sprite, (col * width, row * height))
    
    return surface

def create_all_default_sprites():
    """Create all necessary default sprite sheets"""
    pygame.init()
    
    # Ensure directory exists
    sprite_dir = os.path.join("assets", "Sprite")
    if not os.path.exists(sprite_dir):
        os.makedirs(sprite_dir)
    
    # Create character sprites with fixed dimensions
    for filename, (width, height, rows, cols, color) in {
        "npc_sheet.png": (32, 48, 4, 12, (200, 200, 200)),      # NPCs in gray
        "monster_sheet.png": (48, 48, 4, 12, (255, 100, 100)),  # Monsters in red
        "player_sheet.png": (32, 48, 4, 12, (100, 100, 255)),   # Player in blue
    }.items():
        surface = create_default_sprite_sheet(filename, width, height, rows, cols, color)
        path = os.path.join(sprite_dir, filename)
        pygame.image.save(surface, path)
        print(f"Created {path}")
    
    for filename, ((width, height), (rows, cols), color) in sheets.items():
        surface = create_default_sprite_sheet(width, height, rows, cols, color)
        path = os.path.join("assets/Sprite", filename)
        pygame.image.save(surface, path)
        print(f"Created {path}")

if __name__ == "__main__":
    create_all_default_sprites()
