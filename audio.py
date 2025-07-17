import pygame
import os

class AudioManager:
    def __init__(self):
        # Gunakan dummy audio jika error
        try:
            pygame.mixer.init()
            self.audio_disabled = False
        except pygame.error as e:
            print(f"[WARNING] Audio disabled: {e}")
            os.environ["SDL_AUDIODRIVER"] = "dummy"
            self.audio_disabled = True
            return

        # Load sound hanya jika audio tersedia
        self.sounds = {}
        try:
            self.sounds = {
                "creak": pygame.mixer.Sound("audio/creaking_door.wav"),
                "whisper": pygame.mixer.Sound("audio/whisper.wav"),
            }
        except pygame.error as e:
            print(f"[WARNING] Failed loading sounds: {e}")

    def play_sound(self, sound_name):
        if not self.audio_disabled and sound_name in self.sounds:
            self.sounds[sound_name].play()

    def play_music(self, music_path, loop=-1):
        if not self.audio_disabled:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loop)

    def stop_music(self):
        if not self.audio_disabled:
            pygame.mixer.music.stop()
