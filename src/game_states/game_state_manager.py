import pygame
from engine.engine import Engine
from game_logic.game_stats import GameStats
from game_logic.world_manager import WorldManager
from game_states import game, main_menu, opening_screen
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


        self.timer = 300


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

    def opening_screen(self):
        self.timer -= self.engine.get_delta()

        self.drawing_man.draw_image(self.image, 0, 0)

        if self.timer <= 0:
            self.state = GameState.MAIN_MENU
