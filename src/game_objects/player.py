from objects.base_object import BaseObject
import pygame, sys


class Player(BaseObject):
    
    def __init__(self, x, y):
        super().__init__(x, y, 0, 16, 16)

    def update(self):


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 1
        if keys[pygame.K_RIGHT]:
            self.x += 1
        if keys[pygame.K_UP]:
            self.y -= 1
        if keys[pygame.K_DOWN]:
            self.y += 1
        