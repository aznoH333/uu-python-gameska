import pygame, sys

from engine.engine import Engine
from game_objects.player import Player
from objects.object_manager import ObjectManager
from sprites.sprite_manager import SpriteManager
from world.world_manager import WorldManager

pygame.init()
pygame.display.set_caption("Python gameska")


# init managers
sprite_man = SpriteManager.get_instance()
obj_man = ObjectManager.get_instance()
engine = Engine.get_instance()
world = WorldManager.get_instance()

# spawn player
obj_man.add_object(Player(0, 0))


while True:
    engine.update()
    sprite_man.update_screen()
    
    world.update()
    obj_man.update()
    pygame.display.flip()
    