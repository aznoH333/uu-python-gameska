from engine.engine import Engine
from objects.base_object import BaseObject
import pygame


class Player(BaseObject):
    
    def __init__(self, x, y):
        super().__init__(x, y, 0, 16, 16)
        self.engine = Engine.get_instance()

    def update(self):


        if self.engine.is_key_down(pygame.K_LEFT):
            self.x -= self.engine.get_delta() * 5
        if self.engine.is_key_down(pygame.K_RIGHT):
            self.x += self.engine.get_delta() * 5
        if self.engine.is_key_down(pygame.K_UP):
            self.y -= self.engine.get_delta() * 5
        if self.engine.is_key_down(pygame.K_DOWN):
            self.y += self.engine.get_delta() * 5

        