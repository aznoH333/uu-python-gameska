import pygame, sys

from game_objects.player import Player
from objects.object_manager import ObjectManager
from sprites.sprite_manager import SpriteManager

pygame.init()
pygame.display.set_caption("Hello World")

sprite_man = SpriteManager.get_instance()
obj_man = ObjectManager.get_instance()
obj_man.add_object(Player(200, 200))
while True:
   
    sprite_man.update_screen()
    for i in range(0, 24):
        sprite_man.draw_sprite(i, i*64, 0)
    
    obj_man.update()

    pygame.display.flip()

    

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()