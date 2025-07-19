import pygame

class SpriteAnimation:
    def __init__(self):
        self.animations = {}
        self.current_frame = 0
        self.animation_timer = 0
        self.frame_duration = 100  # milliseconds per frame
        
    def load_sprite_sheet(self, sheet_path, sprite_width, sprite_height, colorkey=(0, 255, 0)):
        """Load a sprite sheet and split it into individual frames"""
        try:
            sheet = pygame.image.load(sheet_path).convert()
            sheet.set_colorkey(colorkey)
            
            sheet_width = sheet.get_width()
            sheet_height = sheet.get_height()
            
            frames = []
            for y in range(0, sheet_height, sprite_height):
                for x in range(0, sheet_width, sprite_width):
                    frame = pygame.Surface((sprite_width, sprite_height))
                    frame.blit(sheet, (0, 0), (x, y, sprite_width, sprite_height))
                    frame.set_colorkey(colorkey)
                    frames.append(frame)
            
            return frames
        except Exception as e:
            print(f"Error loading sprite sheet: {e}")
            return []

    def add_animation(self, name, frames, loop=True):
        """Add a new animation sequence"""
        self.animations[name] = {
            'frames': frames,
            'loop': loop,
            'frame_count': len(frames)
        }

    def update(self, delta_time):
        """Update the current animation frame"""
        self.animation_timer += delta_time
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.current_animation['frames']):
                if self.current_animation['loop']:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.current_animation['frames']) - 1

    def get_current_frame(self):
        """Get the current animation frame"""
        if self.current_animation and self.current_frame < len(self.current_animation['frames']):
            return self.current_animation['frames'][self.current_frame]
        return None

    def set_animation(self, name):
        """Set the current animation"""
        if name in self.animations and (not hasattr(self, 'current_animation') or 
                                      self.current_animation != self.animations[name]):
            self.current_animation = self.animations[name]
            self.current_frame = 0
            self.animation_timer = 0

class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet_path, sprite_width, sprite_height):
        super().__init__()
        self.animator = SpriteAnimation()
        self.load_animations(sprite_sheet_path, sprite_width, sprite_height)
        self.rect = pygame.Rect(x, y, sprite_width, sprite_height)
        self.direction = "down"
        self.state = "idle"
        
    def load_animations(self, sprite_sheet_path, sprite_width, sprite_height):
        frames = self.animator.load_sprite_sheet(sprite_sheet_path, sprite_width, sprite_height)
        if frames:
            # Split frames into different animations
            self.animator.add_animation("idle_down", frames[0:4])
            self.animator.add_animation("idle_up", frames[4:8])
            self.animator.add_animation("idle_left", frames[8:12])
            self.animator.add_animation("idle_right", frames[12:16])
            self.animator.add_animation("walk_down", frames[16:24])
            self.animator.add_animation("walk_up", frames[24:32])
            self.animator.add_animation("walk_left", frames[32:40])
            self.animator.add_animation("walk_right", frames[40:48])
            self.animator.add_animation("attack_down", frames[48:52], loop=False)
            self.animator.add_animation("attack_up", frames[52:56], loop=False)
            self.animator.add_animation("attack_left", frames[56:60], loop=False)
            self.animator.add_animation("attack_right", frames[60:64], loop=False)
            
    def update(self, delta_time):
        animation_name = f"{self.state}_{self.direction}"
        self.animator.set_animation(animation_name)
        self.animator.update(delta_time)
        self.image = self.animator.get_current_frame()
        
    def set_state(self, state):
        if state != self.state:
            self.state = state
            
    def set_direction(self, direction):
        if direction != self.direction:
            self.direction = direction
