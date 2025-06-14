import math
from engine.engine import Engine
from engine.utils import gravitate_number, signum
from objects.base_object import BaseObject
import pygame
from sprites.drawing_manager import DrawingManager
from world.world_manager import WorldManager


class Player(BaseObject):
    

    SPEED = 5
    ACCELERATION = 0.1
    GRAVITY = 0.1

    def __init__(self, x, y):
        super().__init__(x, y, 0, 20, 30, -6, 2)
        self.engine = Engine.get_instance()
        self.world = WorldManager.get_instance()
        self.drawing_man = DrawingManager.get_instance()
        self.xm = 0
        self.ym = 0
        self.tile_bellow = False
        self.tile_left = False
        self.tile_right = False

    def update(self):

        # accelerate
        if self.engine.is_key_down(pygame.K_LEFT):
            self.xm = gravitate_number(self.xm, -self.SPEED, self.ACCELERATION)
        elif self.engine.is_key_down(pygame.K_RIGHT):
            self.xm = gravitate_number(self.xm, self.SPEED, self.ACCELERATION)
        else:
            self.xm = gravitate_number(self.xm, 0, self.ACCELERATION)


        # gravity and on ground stuff
        self.tile_bellow = self.world.collides_with_tile(self.x, self.y + self.ym + 1, self.width, self.height)
        self.tile_left = self.x + self.xm > 0 and self.world.collides_with_tile(self.x - self.xm - 1, self.y, self.width, self.height)
        self.tile_right = self.x + self.xm + self.width + (self.width / 2)< self.world.TOTAL_WIDTH and self.world.collides_with_tile(self.x + self.xm + 1, self.y, self.width, self.height)

        # horizontal collisions
        if self.world.collides_with_tile(self.x + self.xm + signum(self.xm), self.y, self.width, self.height):
            self.xm = 0

        # vertical collisions
        if self.world.collides_with_tile(self.x, self.y + self.ym + signum(self.ym), self.width, self.height) or self.tile_bellow:
            self.ym = 0
        else:
            self.ym += self.GRAVITY




        # update values
        self.x += self.xm 
        self.y += self.ym


        # unstuck player
        if self.world.collides_with_tile(self.x, self.y, self.width, self.height):
            self.y -= 1

        #mining
        if self.engine.is_key_down(pygame.K_DOWN) and self.tile_bellow:
            self.world.damage_tile(self.x, self.y + self.height)

        if self.engine.is_key_down(pygame.K_LEFT) and self.tile_left:
            self.world.damage_tile(self.x - (self.width / 2), self.y + (self.height / 2))
            
        if self.engine.is_key_down(pygame.K_RIGHT) and self.tile_right:
            self.world.damage_tile(self.x + self.width + (self.width / 2), self.y + (self.height / 2))


        
        # world progress
        if self.world.convert_to_world_y(self.y) > 200:
            self.world.progress_by(self.world.convert_to_world_y(self.y) - 200)


        #debug
        self.drawing_man.draw_text(f"{self.tile_left} {self.x + self.xm > 0}", 60, 60)

    
