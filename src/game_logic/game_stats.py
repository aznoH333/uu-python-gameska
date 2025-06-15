import math
from engine.utils import clamp_value
from game_logic.world_manager import WorldManager
from sprites.drawing_manager import DrawingManager


class GameStats:
    instance = None 
    def get_instance():
        if GameStats.instance == None:
            GameStats.instance = GameStats()
        return GameStats.instance
    
    def __init__(self):
        self.money = 0
        self.world_man = WorldManager.get_instance()
        self.drawing_man = DrawingManager.get_instance()
        self.fuel = 50
        self.fuel_max = 50
        self.fuel_efficiency = 1
        
        pass

    def update(self):

        self.drawing_man.draw_text(f"Hloubka {round(self.world_man.get_depth() / 6.4)}m", 30, 42)
        self.drawing_man.draw_text(f"Prachy {self.money}$", 30, 74, (213, 171, 7))
        self.drawing_man.draw_text(f"Palivo {math.ceil(self.fuel)} / {self.fuel_max}", 30, 106)

    def add_money(self, ammount):
        self.money += ammount

    def add_fuel(self, ammount):
        self.fuel = clamp_value(self.fuel + ammount, 0, self.fuel_max)

    def get_fuel_efficiency(self):
        return 1 - (self.fuel_efficiency / 100)