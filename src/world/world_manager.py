import math
from engine.engine import Engine
from sprites.sprite_manager import SpriteManager
from world.tile import Tile


class WorldManager:
    instance = None

    TILE_SIZE = 32

    def get_instance():
        if WorldManager.instance == None:
            WorldManager.instance = WorldManager()

        return WorldManager.instance
    


    WORLD_WIDTH = 20
    WORLD_HEIGHT = 13
    TOTAL_WIDTH = WORLD_WIDTH * TILE_SIZE

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
                self.tiles[y][x].draw(self.sprite_man, x * self.TILE_SIZE, y * self.TILE_SIZE - self.world_offset)

        # progress map
        if self.depth < self.progress_to:
            self.depth += self.progress_speed
            self.world_offset += self.progress_speed

            if self.world_offset > self.TILE_SIZE:
                self.world_offset -= self.TILE_SIZE
                self.shift_world_up()
                self.fill_tiles(self.WORLD_HEIGHT - 1)


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

    def get_tile_from_world_coord(self, x, y):
        return self.tiles[y % self.WORLD_HEIGHT][x]


    def collides_with_tile(self, x, y, w, h):
        y = self.convert_to_world_y(y)
        
        start_x = math.floor(x / self.TILE_SIZE)
        start_y = math.floor(y / self.TILE_SIZE)
        # nemame technologii na for (int i = 0; i <= 1; i++)
        end_x = start_x + 1 + math.ceil(w / self.TILE_SIZE)
        end_y = start_y + 1 + math.ceil(h / self.TILE_SIZE)


        if start_x < 0 or end_x > self.WORLD_WIDTH:
            return True


        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile = self.get_tile_from_world_coord(x, y)

                if tile.is_solid():
                    return True
        
        return False
    
    def convert_to_world_y(self, y):
        return y - self.depth + self.world_offset
    
    def get_depth(self):
        return self.depth
    


    def damage_tile(self, x, y):
        converted_x = round((x + (self.TILE_SIZE / 2)) / self.TILE_SIZE)
        converted_y = round((y + (self.TILE_SIZE / 2)) / self.TILE_SIZE)
        if converted_x < 0 or converted_x > self.WORLD_WIDTH:
            return
        
        tile = self.get_tile_from_world_coord(converted_x, converted_y)

        # TODO tile toughness
        tile.set_tile(False, 1)