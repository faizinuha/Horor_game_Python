
import pygame
class AudioManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.sounds = {
                "scream": pygame.mixer.Sound("audio/whisper.wav.wav"),
            }
        except:
            print("[WARNING] Audio disabled: Error loading sounds")
            self.sounds = {}

    def play_sound(self, key):
        if key in self.sounds:
            self.sounds[key].play()
