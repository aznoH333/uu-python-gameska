import pygame, sys

from engine.engine import Engine
from game_objects.player import Player
from objects.object_manager import ObjectManager
from sprites.sprite_manager import SpriteManager

pygame.init()
pygame.display.set_caption("Hello World")


# init managers
sprite_man = SpriteManager.get_instance()
obj_man = ObjectManager.get_instance()
engine = Engine.get_instance()

# spawn player
obj_man.add_object(Player(0, 0))


while True:
   
    engine.update()
    sprite_man.update_screen()
    for i in range(0, 24):
        sprite_man.draw_sprite(i, i*32, 0)
    
    obj_man.update()



    pygame.display.flip()

    