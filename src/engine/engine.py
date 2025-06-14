import math
import sys
import pygame
clock = pygame.time.Clock()


class Engine:
    instance = None

    def get_instance():
        if Engine.instance == None:
            Engine.instance = Engine()
        return Engine.instance
    
    def __init__(self):
        self.delta = 0
        self.tick_time = 0
        self.last_tick_time = 0
        self.timer = 0
        self.keys = None
        self.is_game_running = True
        
        pass


    def update(self):
        
        # poll events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        
        # poll inputs
        self.keys = pygame.key.get_pressed()


        # calculate delta
        self.tick_time = pygame.time.get_ticks()
        self.delta = (self.tick_time - self.last_tick_time) / 16.6666 # simulate 60 fps
        self.last_tick_time = self.tick_time

        self.timer += self.delta

    def get_delta(self):
        return self.delta
    
    def get_global_timer(self):
        return math.floor(self.timer)
    
    def is_key_down(self, key):
        return self.keys[key]
    

