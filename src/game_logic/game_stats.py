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
        
        pass

    def update(self):

        self.drawing_man.draw_text(f"Hloubka {round(self.world_man.get_depth() / 6.4)}m", 30, 42)
        self.drawing_man.draw_text(f"Prachy {self.money}", 30, 74)
