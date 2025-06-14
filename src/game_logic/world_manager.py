import math
from engine.engine import Engine
from game_objects.rock_particle import RockParticle
from sprites.drawing_manager import DrawingManager
from game_logic.tile import Tile
import random


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
        self.drawing_man = DrawingManager.get_instance()
        self.engine = Engine.get_instance()
        self.obj_man = None

        # prefill with tiles
        for i in range(0, self.WORLD_HEIGHT):
            self.tiles.append([])
            for j in range(0, self.WORLD_WIDTH):
                self.tiles[i].append(Tile())

        for i in range(6, self.WORLD_HEIGHT):
            self.fill_tiles(i)

    def update(self):
        # draw tiles
        for y in range(0, self.WORLD_HEIGHT):
            for x in range(0, self.WORLD_WIDTH):
                self.tiles[y][x].draw(self.drawing_man, x * self.TILE_SIZE, y * self.TILE_SIZE - self.world_offset)

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
            tile.set_tile(True, 0, (170, 170, 255), 50)

    def shift_world_up(self):
        temp = self.tiles[0]

        for i in range(1, self.WORLD_HEIGHT):
            self.tiles[i - 1] = self.tiles[i]

        self.tiles[self.WORLD_HEIGHT - 1] = temp

    def get_tile_from_world_coord(self, x, y):
        return self.tiles[y % self.WORLD_HEIGHT][x]


    def collides_with_tile(self, x, y, w, h, debug_draw = False):
        y = self.convert_to_world_y(y)
        

        # this could be optimized if i bothered to learn for loops properly
        # oh well
        # the c version of this would use conditional step size
        # hovewer we dont have the technology to do that in python
        for x_iterator in range(math.floor(x), math.ceil(x+w)+1):
            for y_iterator in range(math.floor(y), math.ceil(y+h)+1):
                converted_x = math.floor(x_iterator / self.TILE_SIZE)
                converted_y = math.floor(y_iterator / self.TILE_SIZE)

                if debug_draw:
                    self.drawing_man.draw_debug_pixel(x_iterator, y_iterator - self.world_offset, (255, 255, 255))

                if converted_x < 0 or converted_x >= self.WORLD_WIDTH or self.get_tile_from_world_coord(converted_x, converted_y).is_solid():
                    return True
        
        return False
    
    def convert_to_world_y(self, y):
        return y - self.depth + self.world_offset
    
    def get_depth(self):
        return self.depth
    


    def damage_tile(self, x, y, mining_power):
        # find tile
        converted_x = round(x / self.TILE_SIZE)
        converted_y = round(self.convert_to_world_y(y) / self.TILE_SIZE)
        if converted_x < 0 or converted_x > self.WORLD_WIDTH:
            return
        
        tile = self.get_tile_from_world_coord(converted_x, converted_y)
        # check if exists
        if not tile.is_solid():
            return
        
        # damage tile
        self.drawing_man.add_screen_shake(3)
        tile.deal_damage(mining_power)

        particle_x = round(x / self.TILE_SIZE) * self.TILE_SIZE + (self.TILE_SIZE / 2)
        particle_y = round(y / self.TILE_SIZE) * self.TILE_SIZE + (self.TILE_SIZE / 2)
        for _ in range(0, random.randint(2, 4)):
            self.obj_man.add_object(RockParticle(particle_x + random.randint(-6, 6), particle_y + random.randint(-6, 6), tile.get_particle_color()))
        # kill tile
        if not tile.is_stable():
            for _ in range(0, random.randint(6, 8)):
                self.obj_man.add_object(RockParticle(particle_x + random.randint(-6, 6), particle_y + random.randint(-6, 6), tile.get_particle_color()))

            tile.set_tile(False, 1)
            self.drawing_man.add_screen_shake(5)


        

            