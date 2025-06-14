import pygame

from engine.engine import Engine
from game_objects.player import Player
from objects.object_manager import ObjectManager
from sprites.drawing_manager import DrawingManager
from world.world_manager import WorldManager

pygame.init()
pygame.display.set_caption("Python gameska")


# init managers
drawing_man = DrawingManager.get_instance()
obj_man = ObjectManager.get_instance()
engine = Engine.get_instance()
world = WorldManager.get_instance()

# spawn player
obj_man.add_object(Player(0, 0))



while True:
    engine.update()
    drawing_man.update_screen()
    
    if engine.is_key_down(pygame.K_SPACE):
        world.progress_by(1)

    world.update()
    obj_man.update()
    pygame.display.flip()
    