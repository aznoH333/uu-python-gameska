import math
import pygame
from engine.engine import Engine
from game_logic.game_stats import GameStats
from game_logic.world_manager import WorldManager
from game_sounds.sounds_manager import SoundManager
from game_states.game_state import GameState
from objects.object_manager import ObjectManager
from sprites.drawing_manager import DrawingManager


class GameStateManager:
    instance = None

    def get_instance():
        if GameStateManager.instance == None:
            GameStateManager.instance = GameStateManager()
        return GameStateManager.instance
    

    def __init__(self):
        # NOTE: this code kind of sucks but i am tired at this point
        self.state = GameState.OPENING_SCREEN
        self.obj_man = ObjectManager.get_instance()
        self.world = WorldManager.get_instance()
        self.game_stats = GameStats.get_instance()
        self.drawing_man = DrawingManager.get_instance()
        self.engine = Engine.get_instance()
        self.image = pygame.image.load("./sprites/Among.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.image.set_alpha(0)
        self.sound_manager = SoundManager.get_instance()


        self.timer = 240 # 4 seconds


    def update(self):
        match(self.state):
            case GameState.OPENING_SCREEN:
                self.opening_screen()
            case GameState.GAME:
                self.game()
            case GameState.MAIN_MENU:
                self.main_menu()


    

    def game(self):
        self.world.update()
        self.obj_man.update()
        self.game_stats.update()

    def main_menu(self):
        pass

    def opening_screen(self):
        self.timer -= self.engine.get_delta()

        self.drawing_man.draw_image(self.image, 272, 132)


        alpha = math.sin(self.timer / 180 * math.pi) * 255
        self.image.set_alpha(alpha)
        if self.timer <= 0:
            self.state = GameState.MAIN_MENU
            self.sound_manager["music"].play(-1).set_volume(1)
