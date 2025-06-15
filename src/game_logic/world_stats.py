import math
from engine.utils import fade_color, pick_random_color


class WorldStats:
    def __init__(self, depth):
        self.color = None
        self.toughness = None
        self.start = 0     
        self.generate_new(depth)   


    def generate_new(self, depth):
        self.start = depth
        self.color = fade_color(pick_random_color(), 0.75)
        self.toughness = 10 + (math.log(depth + 100) * 10)

    def has_reached(self, depth):
        return depth >= self.start
    
    def get_start_depth(self):
        return self.start