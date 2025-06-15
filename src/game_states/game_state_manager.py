import math
import random
import pygame
from engine.engine import Engine
from engine.utils import box_collision
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
        self.timer += self.engine.get_delta() * 2
        alpha = min(self.timer, 255)
        self.drawing_man.draw_text("Video hra", 270, 100, (alpha, alpha, alpha, alpha))
        
        
        
        self.button("Start", 290, 180, alpha, self.start)
        self.button("Konec", 290, 210, alpha, self.end_me)
        """
            Jakub Tesař (7054-6495-1)
    Lukáš Nový (4439-6070-1)
    Do Ngoc Linh (216-1914-1)
    Jan Laššák (3753-7875-1)
    Eva Masáková (9939-5890-1)
        """
        self.drawing_man.draw_text("Ovládání: Šipky", 30, 300, (alpha, alpha, alpha, alpha))

        self.drawing_man.draw_text("Autoři: Jan Laššák, Jakub Tesař, Lukáš Nový, Eva Masáková, Do Ngoc Linh", 30, 340, (alpha, alpha, alpha, alpha))


    def opening_screen(self):
        self.timer -= self.engine.get_delta()

        self.drawing_man.draw_image(self.image, 272, 132)


        alpha = math.sin(self.timer / 180 * math.pi) * 255
        self.image.set_alpha(alpha)
        if self.timer <= 0:
            self.state = GameState.MAIN_MENU
            
            

            self.timer = 0

    def button(self, text, x, y, alpha, function):
        mouse_pos = pygame.mouse.get_pos()

        selected = box_collision(mouse_pos[0] / 2, mouse_pos[1] / 2, 1, 1, x, y - 20, len(text) * 10, 30)

        if selected and pygame.mouse.get_pressed(num_buttons=3)[0]:
            function()
        self.drawing_man.draw_text(text, x, y, (alpha, alpha, alpha * (not selected), alpha))

    def start(self):
        music = ["music_alt", "music"][random.randint(0, 1)]
            
        self.sound_manager[music].play(-1).set_volume(1)

        self.state = GameState.GAME

    
    def end_me(self):
        pygame.quit()