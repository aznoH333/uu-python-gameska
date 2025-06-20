import math
import pygame

from engine.engine import Engine
from engine.utils import fade_color, gravitate_number


class DrawingManager:

    instance = None

    SPRITE_SCALE = 32
    GAME_ZOOM = 2

    def get_instance():
        if DrawingManager.instance == None:
            DrawingManager.instance = DrawingManager()
        return DrawingManager.instance
    

    def __init__(self):
        self.sprite_sheet = pygame.image.load("./sprites/spritesheet.png")
        self.sprite_sheet_width = self.sprite_sheet.get_rect().width / self.SPRITE_SCALE
        self.sprite_sheet_height = self.sprite_sheet.get_rect().height / self.SPRITE_SCALE
        self.screen = pygame.display.set_mode((1280, 720))
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (self.sprite_sheet_width * self.SPRITE_SCALE * self.GAME_ZOOM, self.sprite_sheet_height * self.SPRITE_SCALE * self.GAME_ZOOM))
        
        self.coloring_surface = pygame.Surface((self.SPRITE_SCALE * self.GAME_ZOOM, self.SPRITE_SCALE * self.GAME_ZOOM))
        pygame.font.init()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.screen_shake = 0
        self.engine = Engine.get_instance()

    """
        Important note.

        Sprite in this context refers to a 2d image drawn to a screen.
        As far as i know this is industry standard terminology.
        Pygame sprites act more like game objects, they have their own logic and lifecycle. 
        SpriteManager doesn't use pygame sprites it uses old fashioned sprites.
        There is no game logic here. If you are looking for that checkout ObjectManager and game objects
    """
    def draw_sprite(self, index, x, y, color=(255, 255, 255)):
        rect = ((index % self.sprite_sheet_width) * self.SPRITE_SCALE * self.GAME_ZOOM,                 #x
                math.floor(index / self.sprite_sheet_width) * self.SPRITE_SCALE * self.GAME_ZOOM,       #y
                self.SPRITE_SCALE * self.GAME_ZOOM,                                                     #w
                self.SPRITE_SCALE * self.GAME_ZOOM                                                      #h
                )
        
        self.coloring_surface.fill(color)
        self.coloring_surface.set_colorkey((0, 0, 0, 0))
        self.coloring_surface.blit(self.sprite_sheet, (0, 0), rect, special_flags=pygame.BLEND_RGBA_MULT)
        
        self.screen.blit(self.coloring_surface, (x * self.GAME_ZOOM, y * self.GAME_ZOOM + (math.sin(self.screen_shake) * (math.sqrt(self.screen_shake + 1)))))

    def draw_image(self, image, x, y):
        self.screen.blit(image, (x * self.GAME_ZOOM, y * self.GAME_ZOOM + (math.sin(self.screen_shake) * (math.sqrt(self.screen_shake + 1)))))



    def draw_text(self, text_base, x, y, color=(255, 255, 255)):
        x*=self.GAME_ZOOM
        y*=self.GAME_ZOOM
        text = self.font.render(text_base, False, color)
        text_rect = text.get_rect()
        text_rect.bottomleft = (x, y)

        text_shadow = self.font.render(text_base, False, fade_color(color, 0.25))
        text_shadow_rect = text_shadow.get_rect()
        text_shadow_rect.bottomleft = (x + 3, y + 3)

        self.screen.blit(text_shadow, text_shadow_rect)
        self.screen.blit(text, text_rect)

    def update_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen_shake = gravitate_number(self.screen_shake, 0, self.engine.get_delta())

    def draw_debug_pixel(self, x, y, color):
        self.coloring_surface.fill(color)
        self.screen.blit(self.coloring_surface, (x * self.GAME_ZOOM, y * self.GAME_ZOOM), (0, 0, self.GAME_ZOOM, self.GAME_ZOOM))

    def add_screen_shake(self, ammount):
        self.screen_shake += ammount