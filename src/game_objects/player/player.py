import math
from engine.engine import Engine
from engine.utils import gravitate_number, signum
from game_logic.game_stats import GameStats
from game_objects.player.player_direction import PlayerDirection
from objects.base_object import BaseObject
import pygame
from sprites.drawing_manager import DrawingManager
from game_logic.world_manager import WorldManager


class Player(BaseObject):
    
    LEFT_SPRITE_INDEX = 18
    RIGHT_SPRITE_INDEX = 22
    DOWN_SPRITE_INDEX = 20
    BASE_Y_OFFSET = -10
    DOWN_Y_OFFSET = -5

    SPEED = 3
    ACCELERATION = 0.1
    GRAVITY = 0.1
    JUMP_STRENGTH = 3.5
    MINING_COOLDOWN = 5

    def __init__(self, x, y):
        super().__init__(x, y, self.RIGHT_SPRITE_INDEX, 20, 20, -6, -10)
        self.engine = Engine.get_instance()
        self.world = WorldManager.get_instance()
        self.drawing_man = DrawingManager.get_instance()
        self.xm = 0
        self.ym = 0
        self.tile_bellow = False
        self.tile_left = False
        self.tile_right = False
        self.direction = PlayerDirection.RIGHT
        self.mining_power = 10 # TODO : mining power upgrades
        self.mining_cooldown = 0
        self.game_stats = GameStats.get_instance()

    def update(self):
        delta = self.engine.get_delta()
        # accelerate
        if self.engine.is_key_down(pygame.K_LEFT):
            self.xm = gravitate_number(self.xm, -self.SPEED, self.ACCELERATION * delta)
            self.direction = PlayerDirection.LEFT
        elif self.engine.is_key_down(pygame.K_RIGHT):
            self.xm = gravitate_number(self.xm, self.SPEED, self.ACCELERATION * delta)
            self.direction = PlayerDirection.RIGHT
        else:
            self.xm = gravitate_number(self.xm, 0, self.ACCELERATION * delta)


        # gravity and on ground stuff
        self.tile_bellow = self.world.collides_with_tile(self.x, self.y + 1, self.width, self.height)
        self.tile_left = self.x + self.xm > 0 and self.world.collides_with_tile(self.x + self.xm - 1, self.y, self.width, self.height)
        self.tile_right = self.x + self.xm + self.width + (self.width / 2)< self.world.TOTAL_WIDTH and self.world.collides_with_tile(self.x + self.xm + 1, self.y, self.width, self.height)

        # jumping
        if self.tile_bellow and self.engine.is_key_down(pygame.K_UP):
            self.tile_bellow = False 
            self.ym = -self.JUMP_STRENGTH


        # horizontal collisions
        if self.world.collides_with_tile(self.x + self.xm + signum(self.xm), self.y, self.width, self.height):
            self.xm = 0

        # vertical collisions
        if self.world.collides_with_tile(self.x, self.y + self.ym + signum(self.ym), self.width, self.height) or self.tile_bellow:
            self.ym = 0
        else:
            self.ym += self.GRAVITY * delta


        

        # update values
        self.x += self.xm * delta
        self.y += self.ym * delta


        # unstuck player
        if self.world.collides_with_tile(self.x, self.y, self.width, self.height):
            self.y -= 1


        #mining

        if self.mining_cooldown <= 0:
            mining_result = (0, False)
            
            if self.engine.is_key_down(pygame.K_DOWN) and self.tile_bellow:
                mining_result = self.world.damage_tile(self.x, self.y + self.height, self.mining_power)
                self.direction = PlayerDirection.DOWN
                self.reset_mining_cooldown()

            if self.engine.is_key_down(pygame.K_LEFT) and self.tile_left and self.tile_bellow:
                mining_result = self.world.damage_tile(self.x - self.width, self.y, self.mining_power)
                self.reset_mining_cooldown()

                
            if self.engine.is_key_down(pygame.K_RIGHT) and self.tile_right and self.tile_bellow:
                mining_result = self.world.damage_tile(self.x + self.width + (self.width / 2), self.y, self.mining_power)
                self.reset_mining_cooldown()
            if mining_result[1]:
                self.game_stats.add_fuel(mining_result[0])
            else:
                self.game_stats.add_money(mining_result[0])
        else:
            self.mining_cooldown -= delta

        


        
        
        # world progress
        if self.world.convert_to_world_y(self.y) > 200:
            self.world.progress_by(self.world.convert_to_world_y(self.y) - 200)




        # update sprite

        self.y_offset = self.BASE_Y_OFFSET

        # i am too lazy to implement sprite flipping so this hacky workaround will be good enough
        match (self.direction):
            case PlayerDirection.LEFT:
                self.sprite_index = self.LEFT_SPRITE_INDEX
            case PlayerDirection.RIGHT:
                self.sprite_index = self.RIGHT_SPRITE_INDEX
            case PlayerDirection.DOWN:
                self.sprite_index = self.DOWN_SPRITE_INDEX
                self.y_offset = self.DOWN_Y_OFFSET

        self.sprite_index += self.engine.get_global_timer() % 20 > 10

    def reset_mining_cooldown(self):
        self.mining_cooldown = self.MINING_COOLDOWN # TODO upgrades
