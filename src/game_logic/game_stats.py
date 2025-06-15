import math
from engine.utils import clamp_value
from sprites.drawing_manager import DrawingManager


class GameStats:
    instance = None 
    def get_instance():
        if GameStats.instance == None:
            GameStats.instance = GameStats()
        return GameStats.instance
    
    def __init__(self):
        self.money = 0
        self.depth = 0
        self.drawing_man = DrawingManager.get_instance()
        self.fuel = 1
        self.max_fuel = 50
        self.fuel_efficiency = 1
        self.mining_power = 10
        self.game_over = False
        
        pass

    def update(self):
        if not self.game_over:
            self.drawing_man.draw_text(f"Hloubka {round(self.depth / 6.4)}m", 30, 42)
            self.drawing_man.draw_text(f"Prachy {self.money}$", 30, 74, (240, 200, 7))
            self.drawing_man.draw_text(f"Palivo {math.ceil(self.fuel)} / {self.max_fuel}L", 30, 106, (173, 0, 255))
            if self.fuel == 0:
                self.game_over = True
        else:
            self.drawing_man.draw_text(f"Konec gamesky :(", 240, 180)
            self.drawing_man.draw_text(f"Došlo ti palivo", 250, 216)


    def add_money(self, ammount):
        self.money += ammount

    def add_fuel(self, ammount):
        self.fuel = clamp_value(self.fuel + ammount, 0, self.max_fuel)

    def get_fuel_efficiency(self):
        return 1 - (min(self.fuel_efficiency, 20) / 20)