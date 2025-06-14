class Tile:
    def __init__(self):
        self.is_visible = False
        self.is_solid = False,
        self.sprite = 0

    def set_tile(self, solid, sprite):
        
        self.is_visible = True
        self.is_solid = solid,
        self.sprite = sprite

    def draw(self, sprite_man, x, y):
        if not self.is_visible:
            return
        sprite_man.draw_sprite(self.sprite, x, y)