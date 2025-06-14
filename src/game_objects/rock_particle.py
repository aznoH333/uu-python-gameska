from engine.engine import Engine
from engine.utils import gravitate_number
from objects.base_object import BaseObject
import random

class RockParticle(BaseObject):

    PARTICLE_START = 24
    PARTICLE_FRAME_COUNT = 3

    SPREAD_X = 1.4
    SPREAD_Y_LOWER = -2.4
    SPREAD_Y_UPPER = 0.4

    GRAVITY = 0.05

    ANIMATION_SPEED = 10

    def __init__(self, x, y, color):
        
        starting_frame = random.randint(1, self.PARTICLE_FRAME_COUNT) - 1
        super().__init__(x, y, starting_frame + self.PARTICLE_START, 0, 0, -16, -16, color)

        self.frame = starting_frame

        self.xm = random.uniform(-self.SPREAD_X, self.SPREAD_X)
        self.ym = random.uniform(self.SPREAD_Y_LOWER, self.SPREAD_Y_UPPER)
        self.timer = 0
        self.life_timer = 280
        self.engine = Engine.get_instance()


    def update(self):
        # update position
        self.ym += self.GRAVITY
        self.x += self.xm
        self.y += self.ym


        self.life_timer -= self.engine.get_delta()
        if self.life_timer < 0:
            self.wants_to_be_alive = False

        # update sprite 
        self.timer += self.engine.get_delta()
        if self.timer > self.ANIMATION_SPEED:
            self.timer -= self.ANIMATION_SPEED
            self.frame += 1
            self.frame %= self.PARTICLE_FRAME_COUNT
            self.sprite_index = self.frame + self.PARTICLE_START
