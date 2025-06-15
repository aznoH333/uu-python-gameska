import math
from engine.engine import Engine
from engine.utils import interpolate, interpolate_color, pick_random_color
from game_logic.ore import Ore
from game_logic.world_stats import WorldStats
from game_objects.rock_particle import RockParticle
from game_objects.value_particle import ValueParticle
from sprites.drawing_manager import DrawingManager
from game_logic.tile import Tile
import random


class WorldManager:
    instance = None

    TILE_SIZE = 32
    DISTANCE_BETWEEN_COLOR_CHANGES = 640

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

        # init colors
        self.current_color = WorldStats(0)
        self.current_color.color = (126, 240, 128)
        self.next_color = WorldStats(self.DISTANCE_BETWEEN_COLOR_CHANGES)


        #init ores
        self.coal_ore = Ore()
        self.coal_ore.set_ore(10, (0,0,0), 8, 1.1, True, True, 0.3)

        self.active_ores = []
        for i in range(0, 2):
            self.generate_ore()


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

        # progress world stats
        if self.next_color.has_reached(self.depth):
            self.current_color = self.next_color
            self.next_color = WorldStats(self.depth + self.DISTANCE_BETWEEN_COLOR_CHANGES)
            self.generate_ore()

            if len(self.active_ores) > 6:
                for i in range(0, 3):
                    index = random.randint(0, len(self.active_ores))
                    del self.active_ores[index]


    def progress_by(self, value):
        self.progress_to = self.depth + value

    def fill_tiles(self, y):
        
        progress = (self.depth - self.current_color.get_start_depth()) / (self.next_color.get_start_depth() - self.current_color.get_start_depth())
        color = interpolate_color(self.current_color.color, self.next_color.color, progress)
        toughness = interpolate(self.current_color.toughness, self.next_color.toughness, progress)
        for x in range(0, self.WORLD_WIDTH):
            tile = self.tiles[y][x]
            tile.set_tile(True, 0, color, toughness)

            ore = self.try_generating_ore_for_tile()

            if ore != None:
                tile.set_ore(ore.sprite, ore.color, ore.value, ore.toughness_multiplier, ore.exists, ore.is_coal, ore.rarity)
            else:
                tile.set_ore(0, 0, 0, 0, False, 0, 0)

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
            return (0, False)
        
        tile = self.get_tile_from_world_coord(converted_x, converted_y)
        # check if exists
        if not tile.is_solid():
            return (0, False)
        
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
            self.drawing_man.add_screen_shake(5)
            value_text = tile.get_mine_text()

            if value_text != None:
                self.obj_man.add_object(ValueParticle(particle_x, particle_y, value_text[1], value_text[0]))
            
            is_coal = tile.is_coal()
            return (int(math.floor(tile.break_tile())), is_coal)
        return (0, False)

        

    def generate_ore(self):
        ore = Ore()
        sprite = random.randint(3, 9)
        color = pick_random_color()
        rarity = random.uniform(0.1, 0.9)
        value = math.floor((200 + (math.pow(1.5 - rarity, 2) * 600)) + (self.depth))
        
        ore.set_ore(sprite, color, value, 1 + (1-rarity), True, False, rarity)
        self.active_ores.append(ore)

    def try_generating_ore_for_tile(self):
        if random.uniform(0, 1) > 0.25:
            return None
        
        if random.uniform(0, 1) < self.coal_ore.rarity: # generate coal
            return self.coal_ore
        
        for ore in self.active_ores:
            if random.uniform(0, 1) < ore.rarity:
                return ore
            
        return None