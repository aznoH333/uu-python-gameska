import pygame
clock = pygame.time.Clock()


class Engine:
    instance = None

    def get_instance():
        if Engine.instance == None:
            Engine.instance = Engine()
        return Engine.instance
    
    def __init__(self):
        self.game_speed = 60
        self.clock = pygame.time.Clock()
        self.delta = 0
        pass

    def set_game_speed(self, speed):
        self.game_speed = speed

    def update(self):
        #TODO poll inputs
        self.delta = self.clock.tick(self.game_speed) / self.game_speed

    def get_delta(self):
        return self.delta