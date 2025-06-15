import pygame

from engine.engine import Engine
from game_logic.game_stats import GameStats
from game_objects.player.player import Player
from game_objects.shop.shop import Shop
from objects.object_manager import ObjectManager
from sprites.drawing_manager import DrawingManager
from game_logic.world_manager import WorldManager
from game_sounds.sounds_manager import SoundManager
from game_menu.ui_element import UIElement


# Colors
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)


# Start Menu Function
def show_start_menu(screen):
    clock = pygame.time.Clock()

    start_button = UIElement(
        center_pos=(screen.get_width() // 2, screen.get_height() // 2),
        text="Start Game",
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE
    )

    while True:
        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and start_button.mouse_over:
                return  # Exit start menu, start game

        mouse_pos = pygame.mouse.get_pos()
        start_button.update(mouse_pos)
        start_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


# Main Game Setup
pygame.init()
pygame.display.set_caption("Python gameska")

# Get DrawingManager's screen
drawing_man = DrawingManager.get_instance()
screen = drawing_man.screen

# Show Start Menu
show_start_menu(screen)


# Initialize Managers
engine = Engine.get_instance()
obj_man = ObjectManager.get_instance()
world = WorldManager.get_instance()
game_stats = GameStats.get_instance()
game_sounds = SoundManager.get_instance()

# Spawn player
obj_man.add_object(Player(0, 0))


# Main Game Loop
while True:
    engine.update()
    drawing_man.update_screen()  # screen is cleared here

    world.update()
    obj_man.update()
    game_stats.update()

    pygame.display.flip()
