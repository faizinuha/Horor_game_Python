import pygame

class AudioManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.sounds = {
                "talk": None,  # Will be created programmatically
                "quest_complete": None,
                "item_pickup": None,
                "footstep": None
            }
            self._create_sounds()
        except:
            print("[WARNING] Audio disabled: Error initializing audio")
            self.sounds = {}

    def _create_sounds(self):
        """Create simple sound effects programmatically"""
        try:
            # Create a simple talk sound (short beep)
            talk_sound = pygame.sndarray.make_sound(self._generate_beep(440, 0.1))
            self.sounds["talk"] = talk_sound
            
            # Create quest complete sound (ascending notes)
            quest_sound = pygame.sndarray.make_sound(self._generate_chord([440, 554, 659], 0.5))
            self.sounds["quest_complete"] = quest_sound
            
            # Create item pickup sound (quick high beep)
            pickup_sound = pygame.sndarray.make_sound(self._generate_beep(880, 0.2))
            self.sounds["item_pickup"] = pickup_sound
            
        except:
            print("[WARNING] Could not create programmatic sounds")

    def _generate_beep(self, frequency, duration):
        """Generate a simple beep sound"""
        import numpy as np
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            wave = np.sin(2 * np.pi * frequency * i / sample_rate)
            # Apply envelope to avoid clicks
            envelope = min(i / (sample_rate * 0.01), 1.0, (frames - i) / (sample_rate * 0.01))
            arr[i] = [wave * envelope * 0.3, wave * envelope * 0.3]
        
        return (arr * 32767).astype(np.int16)

    def _generate_chord(self, frequencies, duration):
        """Generate a chord with multiple frequencies"""
        import numpy as np
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            wave = 0
            for freq in frequencies:
                wave += np.sin(2 * np.pi * freq * i / sample_rate) / len(frequencies)
            
            # Apply envelope
            envelope = min(i / (sample_rate * 0.01), 1.0, (frames - i) / (sample_rate * 0.01))
            arr[i] = [wave * envelope * 0.3, wave * envelope * 0.3]
        
        return (arr * 32767).astype(np.int16)

    def play_sound(self, key):
        if key in self.sounds and self.sounds[key]:
            try:
                self.sounds[key].play()
            except:
                pass  # Ignore audio errors