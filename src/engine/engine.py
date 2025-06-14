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
        self.game_speed = 660
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.timer = 0
        self.keys = None
        self.is_game_running = True

        pass

    def set_game_speed(self, speed):
        self.game_speed = speed

    def update(self):
        
        # poll events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        
        # poll inputs
        self.keys = pygame.key.get_pressed()


        # calculate delta
        self.delta = self.clock.tick(self.game_speed) / self.game_speed
        self.timer += self.delta


    def get_delta(self):
        return self.delta
    
    def get_global_timer(self):
        return math.floor(self.timer)
    
    def is_key_down(self, key):
        return self.keys[key]
    

