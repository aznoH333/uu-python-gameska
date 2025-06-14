import math
import pygame


class SpriteManager:
    """
        Important note.

        Sprite in this context refers to a 2d image drawn to a screen.
        As far as i know this is industry standard terminology.
        Pygame sprites act more like game objects, they have their own logic and lifecycle. 
        SpriteManager doesn't use pygame sprites it uses old fashioned sprites.
        There is no game logic here. If you are looking for that checkout ObjectManager and game objects
    """

    instance = None

    SPRITE_SCALE = 32
    GAME_ZOOM = 2

    def get_instance():
        if SpriteManager.instance == None:
            SpriteManager.instance = SpriteManager()
        return SpriteManager.instance
    

    def __init__(self):
        self.sprite_sheet = pygame.image.load("./sprites/spritesheet.png")
        self.sprite_sheet_width = self.sprite_sheet.get_rect().width / self.SPRITE_SCALE
        self.sprite_sheet_height = self.sprite_sheet.get_rect().height / self.SPRITE_SCALE
        self.screen = pygame.display.set_mode((1280, 720))
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (self.sprite_sheet_width * self.SPRITE_SCALE * self.GAME_ZOOM, self.sprite_sheet_height * self.SPRITE_SCALE * self.GAME_ZOOM))
        self.coloring_surface = pygame.Surface((self.SPRITE_SCALE * self.GAME_ZOOM, self.SPRITE_SCALE * self.GAME_ZOOM))


    def draw_sprite(self, index, x, y, color=(255, 255, 255)):
        rect = ((index % self.sprite_sheet_width) * self.SPRITE_SCALE * self.GAME_ZOOM,                 #x
                math.floor(index / self.sprite_sheet_width) * self.SPRITE_SCALE * self.GAME_ZOOM,       #y
                self.SPRITE_SCALE * self.GAME_ZOOM,                                                     #w
                self.SPRITE_SCALE * self.GAME_ZOOM                                                      #h
                )
        

        self.coloring_surface.fill(color)
        self.coloring_surface.blit(self.sprite_sheet, (0, 0), rect, special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(self.coloring_surface, (x * self.GAME_ZOOM, y * self.GAME_ZOOM))

    def update_screen(self):
        self.screen.fill((0, 0, 0))
