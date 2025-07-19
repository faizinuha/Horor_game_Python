import pygame

class AudioManager:
    def __init__(self):
        self.volume = 0.7  # Default volume
        try:
            pygame.mixer.init(44100, -16, 2, 2048)
            self.sounds = {
                "talk": None,  # Will be created programmatically
                "quest_complete": None,
                "item_pickup": None,
                "footstep": None,
                "menu_select": None,
                "ghost_hit": None,
                "ambient": None,
                "door_creak": pygame.mixer.Sound("audio/creaking_door.wav"),
                "whisper": pygame.mixer.Sound("audio/whisper.wav")
            }
            self._create_sounds()
        except Exception as e:
            print(f"[WARNING] Audio disabled: Error initializing audio - {str(e)}")
            self.sounds = {}

    def _create_sounds(self):
        """Create simple sound effects programmatically"""
        try:
            # Simple beep sounds without numpy
            self.sounds["talk"] = self._create_simple_beep(440, 100)
            self.sounds["quest_complete"] = self._create_simple_beep(660, 300)
            self.sounds["item_pickup"] = self._create_simple_beep(880, 150)
            self.sounds["menu_select"] = self._create_simple_beep(550, 100)
            self.sounds["ghost_hit"] = self._create_simple_beep(220, 500)
            
        except:
            print("[WARNING] Could not create programmatic sounds")

    def _create_simple_beep(self, frequency, duration_ms):
        """Create simple beep without numpy"""
        try:
            import math
            sample_rate = 22050
            frames = int(duration_ms * sample_rate / 1000)
            
            # Create simple sine wave
            arr = []
            for i in range(frames):
                wave = math.sin(2 * math.pi * frequency * i / sample_rate)
                # Simple envelope
                envelope = min(1.0, i / (sample_rate * 0.01), (frames - i) / (sample_rate * 0.01))
                sample = int(wave * envelope * 0.3 * 32767)
                arr.append([sample, sample])
            
            sound_array = pygame.sndarray.make_sound(arr)
            sound_array.set_volume(self.volume)
            return sound_array
        except:
            return None

    def play_sound(self, key):
        if key in self.sounds and self.sounds[key]:
            try:
                self.sounds[key].play()
            except:
                pass  # Ignore audio errors
    
    def adjust_volume(self, change):
        """Adjust volume by change amount"""
        self.volume = max(0.0, min(1.0, self.volume + change))
        # Update volume for all sounds
        for sound in self.sounds.values():
            if sound:
                try:
                    sound.set_volume(self.volume)
                except:
                    pass