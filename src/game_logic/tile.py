import math
import random
from game_logic.ore import Ore


class Tile:
    
    DAMAGE_SPRITE_INDEX = 11
    
    def __init__(self):
        self.is_visible = False
        self.solid = False
        self.sprite = 0
        self.toughness = 30
        self.damage = 0
        self.ore = Ore()

    def set_tile(self, solid, sprite, color = (255, 255, 255), toughness = 1):
        self.is_visible = True
        self.solid = solid
        self.sprite = sprite
        self.toughness = toughness
        self.color = color
        self.damage = 0

    def set_ore(self, sprite, color, value, toughness_multiplier, exists, is_coal, rarity):
        self.ore.set_ore(sprite, color, value, toughness_multiplier, exists, is_coal, rarity)

    def draw(self, drawing_man, x, y):
        if not self.is_visible:
            return
        # main sprite
        drawing_man.draw_sprite(self.sprite, x, y, self.color)

        # ore
        if self.ore.exists:
            color = (255, 255, 255)
            if not self.ore.is_coal:
                color = self.ore.color
            
            drawing_man.draw_sprite(self.ore.sprite, x, y, color)


        # damage sprite
        if self.damage != 0:
            damage_percentage = self.damage / self.toughness
            damage_sprite_index = math.floor(damage_percentage * 3) + self.DAMAGE_SPRITE_INDEX
            drawing_man.draw_sprite(damage_sprite_index, x, y)

    def is_solid(self):
        return self.is_visible and self.solid
    
    def is_stable(self):
        return self.toughness > self.damage
    
    def deal_damage(self, mining_power):
        if self.ore.exists:
            mining_power /= self.ore.toughness_multiplier
        
        self.damage += mining_power 

    def get_particle_color(self):
        color = self.color
        if self.ore.exists and random.uniform(0, 1) > 0.5:
            if self.ore.is_coal:
                color = (44, 30, 49)
            else:
                color = self.ore.color
        
        return color
    
    def break_tile(self):
        self.set_tile(False, 1)
        self.ore.exists = False
        return self.ore.value
    
    def is_coal(self):
        return self.ore.exists and self.ore.is_coal