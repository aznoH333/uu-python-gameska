import pygame

from engine.engine import Engine
from game_logic.game_stats import GameStats
from game_objects.player.player import Player
from game_objects.shop.shop import Shop
from objects.object_manager import ObjectManager
from sprites.drawing_manager import DrawingManager
from game_logic.world_manager import WorldManager

pygame.init()
pygame.display.set_caption("Python gameska")


# init managers
drawing_man = DrawingManager.get_instance()
obj_man = ObjectManager.get_instance()
engine = Engine.get_instance()
world = WorldManager.get_instance()
game_stats = GameStats.get_instance()

# spawn player
obj_man.add_object(Player(0, 0))



while True:
    engine.update()
    drawing_man.update_screen()

    world.update()
    obj_man.update()
    game_stats.update()
    pygame.display.flip()
    