import math


class Tile:
    
    DAMAGE_SPRITE_INDEX = 11
    
    def __init__(self):
        self.is_visible = False
        self.solid = False
        self.sprite = 0
        self.toughness = 30
        self.damage = 0

    def set_tile(self, solid, sprite, color = (255, 255, 255), toughness = 1):
        self.is_visible = True
        self.solid = solid
        self.sprite = sprite
        self.toughness = toughness
        self.color = color
        self.damage = 0

    def draw(self, drawing_man, x, y):
        if not self.is_visible:
            return
        # main sprite
        drawing_man.draw_sprite(self.sprite, x, y, self.color)

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
        self.damage += mining_power

    def get_particle_color(self):
        return self.color # TODO ores