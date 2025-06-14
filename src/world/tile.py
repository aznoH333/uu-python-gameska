class Tile:
    def __init__(self):
        self.is_visible = False
        self.solid = False
        self.sprite = 0

    def set_tile(self, solid, sprite):
        self.is_visible = True
        self.solid = solid
        self.sprite = sprite

    def draw(self, sprite_man, x, y):
        if not self.is_visible:
            return
        sprite_man.draw_sprite(self.sprite, x, y, (255, 10, 41))

    def is_solid(self):
        return self.is_visible and self.solid