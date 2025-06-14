import math
from engine.engine import Engine
from engine.utils import gravitate_number
from objects.base_object import BaseObject
import pygame
from world.world_manager import WorldManager


class Player(BaseObject):
    

    SPEED = 7
    ACCELERATION = 0.5
    GRAVITY = 0.1

    def __init__(self, x, y):
        super().__init__(x, y, 0, 32, 32)
        self.engine = Engine.get_instance()
        self.world = WorldManager.get_instance()
        self.xm = 0
        self.ym = 0
        self.on_ground = False

    def update(self):

        # accelerate
        if self.engine.is_key_down(pygame.K_LEFT):
            self.xm = gravitate_number(self.xm, -self.SPEED, self.ACCELERATION)
        elif self.engine.is_key_down(pygame.K_RIGHT):
            self.xm = gravitate_number(self.xm, self.SPEED, self.ACCELERATION)
        else:
            self.xm = gravitate_number(self.xm, 0, self.ACCELERATION)


        # gravity and on ground stuff
        self.on_ground = self.world.collides_with_tile(self.x, self.y + self.ym + 1, self.width, self.height)
            
        
        if self.on_ground:
            self.ym = 0
            #self.y = self.y - (math.floor(self.y / self.world.TILE_SIZE) * self.world.TILE_SIZE)

        else:
            self.ym += self.GRAVITY




        # update values
        self.x += self.xm 
        self.y += self.ym

    

        