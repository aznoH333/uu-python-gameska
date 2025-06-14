from engine.engine import Engine
from objects.base_object import BaseObject
import pygame


class Player(BaseObject):
    
    def __init__(self, x, y):
        super().__init__(x, y, 0, 16, 16)
        self.engine = Engine.get_instance()

    def update(self):


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.engine.get_delta() * 20
        if keys[pygame.K_RIGHT]:
            self.x += self.engine.get_delta() * 20
        if keys[pygame.K_UP]:
            self.y -= self.engine.get_delta() * 20
        if keys[pygame.K_DOWN]:
            self.y += self.engine.get_delta() * 20
        