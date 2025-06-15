import os
import pygame
from pygame import mixer
from pathlib import Path

BASE_DIR = Path("./")
SOUNDS_DIR = BASE_DIR / "sounds"

class SoundManager:
    instance = None

    def get_instance():
        if SoundManager.instance is None:
            SoundManager.instance = SoundManager()
        return SoundManager.instance

    def __init__(self):

        mixer.init()
        self.sounds = {}

        for file in SOUNDS_DIR.iterdir():
            if file.suffix.lower() in [".wav", ".mp3"]:
                sound_name = file.stem  # filename without extension
                self.sounds[sound_name] = pygame.mixer.Sound(str(file))
                #print(f"Loading: {file.name}")
        self.sounds["music"].play(-1).set_volume(0.7)


    def __getitem__(self, key):
        return self.sounds[key]
