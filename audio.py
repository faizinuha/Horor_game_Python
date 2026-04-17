import pygame

class AudioManager:
    def __init__(self):
        self.volume = 0.7  # Default volume
        self.sounds = {}
        try:
            pygame.mixer.init(44100, -16, 2, 2048)
        except pygame.error as e:
            print(f"[WARNING] Audio disabled: Error initializing mixer - {e}")
            return

        # Programmatic sounds (created below) start as None.
        self.sounds = {
            "talk": None,
            "quest_complete": None,
            "item_pickup": None,
            "footstep": None,
            "menu_select": None,
            "ghost_hit": None,
            "ambient": None,
            "door_creak": None,
            "whisper": None,
        }

        # Load file-based sound effects if they are available. Missing files
        # should not take the whole audio system down.
        for key, path in (
            ("door_creak", "audio/creaking_door.wav"),
            ("whisper", "audio/whisper.wav"),
        ):
            try:
                self.sounds[key] = pygame.mixer.Sound(path)
            except (pygame.error, FileNotFoundError) as e:
                print(f"[WARNING] Could not load {path}: {e}")

        self._create_sounds()

    def _create_sounds(self):
        """Create simple sound effects programmatically"""
        try:
            # Simple beep sounds without numpy
            self.sounds["talk"] = self._create_simple_beep(440, 100)
            self.sounds["quest_complete"] = self._create_simple_beep(660, 300)
            self.sounds["item_pickup"] = self._create_simple_beep(880, 150)
            self.sounds["menu_select"] = self._create_simple_beep(550, 100)
            self.sounds["ghost_hit"] = self._create_simple_beep(220, 500)
        except Exception as e:
            print(f"[WARNING] Could not create programmatic sounds: {e}")

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
        except (pygame.error, ValueError):
            return None

    def play_sound(self, key):
        sound = self.sounds.get(key)
        if sound:
            try:
                sound.play()
            except pygame.error:
                pass  # Ignore audio errors

    def adjust_volume(self, change):
        """Adjust volume by change amount"""
        self.volume = max(0.0, min(1.0, self.volume + change))
        # Update volume for all sounds
        for sound in self.sounds.values():
            if sound:
                try:
                    sound.set_volume(self.volume)
                except pygame.error:
                    pass
