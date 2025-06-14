from engine.engine import Engine
from sprites.sprite_manager import SpriteManager
from world.tile import Tile


class WorldManager:
    instance = None
    def get_instance():
        if WorldManager.instance == None:
            WorldManager.instance = WorldManager()

        return WorldManager.instance
    


    WORLD_WIDTH = 20
    WORLD_HEIGHT = 13

    def __init__(self):
        self.tiles = []
        self.depth = 0
        self.progress_to = 0
        self.progress_speed = 1
        self.world_offset = 0
        self.sprite_man = SpriteManager.get_instance()
        self.engine = Engine.get_instance()

        # prefill with tiles
        for i in range(0, self.WORLD_HEIGHT):
            self.tiles.append([])
            for j in range(0, self.WORLD_WIDTH):
                self.tiles[i].append(Tile())

        for i in range(8, self.WORLD_HEIGHT):
            self.fill_tiles(i)

    def update(self):
        # draw tiles
        for y in range(0, self.WORLD_HEIGHT):
            for x in range(0, self.WORLD_WIDTH):
                self.tiles[y][x].draw(self.sprite_man, x * self.sprite_man.SPRITE_SCALE, y * self.sprite_man.SPRITE_SCALE - self.world_offset)

        # progress map
        if self.depth < self.progress_to:
            self.depth += self.progress_speed
            self.world_offset += self.progress_speed

            if self.world_offset > self.sprite_man.SPRITE_SCALE:
                self.world_offset -= self.sprite_man.SPRITE_SCALE
                self.shift_world_up()


    def progress_by(self, value):
        self.progress_to = self.depth + value

    def fill_tiles(self, y):
        for x in range(0, self.WORLD_WIDTH):
            tile = self.tiles[y][x]
            tile.set_tile(True, 0)

    def shift_world_up(self):
        temp = self.tiles[0]

        for i in range(1, self.WORLD_HEIGHT):
            self.tiles[i - 1] = self.tiles[i]

        self.tiles[self.WORLD_HEIGHT - 1] = temp



    