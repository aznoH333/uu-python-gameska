import pygame

from engine.engine import Engine
from game_logic.game_stats import GameStats
from game_objects.player.player import Player
from game_objects.shop.shop import Shop
from game_states.game_state_manager import GameStateManager
from objects.object_manager import ObjectManager
from sprites.drawing_manager import DrawingManager
from game_logic.world_manager import WorldManager
from game_sounds.sounds_manager import SoundManager


pygame.init()
pygame.display.set_caption("Python gameska")


# init managers
obj_man = ObjectManager.get_instance()
engine = Engine.get_instance()
world = WorldManager.get_instance()
game_stats = GameStats.get_instance()
game_state_manager = GameStateManager.get_instance()
game_sounds = SoundManager.get_instance()
drawing_man = DrawingManager.get_instance()


# spawn player
obj_man.add_object(Player(0, 0))


# Main Game Loop
while True:
    engine.update()
    drawing_man.update_screen()  # screen is cleared here

    game_state_manager.update()

    pygame.display.flip()
