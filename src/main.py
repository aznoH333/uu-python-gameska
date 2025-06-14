import pygame, sys

from sprites.sprite_manager import SpriteManager

pygame.init()
pygame.display.set_caption("Hello World")

sprite_man = SpriteManager.get_instance()

while True:
   
    sprite_man.update_screen()
    for i in range(0, 24):
        sprite_man.draw_sprite(i, i*64, 0)
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()