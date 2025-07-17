
import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "creak": pygame.mixer.Sound("horror_game/audio/creaking_door.wav"),
            "whisper": pygame.mixer.Sound("horror_game/audio/whisper.wav"),
            # Add more sounds here
        }

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def play_music(self, music_path, loop=-1):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(loop)

    def stop_music(self):
        pygame.mixer.music.stop()


