import math
import pygame


class SpriteManager:
    instance = None

    SPRITE_RESOLUTION = 32
    DEFAULT_SCALE = 4

    def get_instance():
        if SpriteManager.instance == None:
            SpriteManager.instance = SpriteManager()
        return SpriteManager.instance
    

    def __init__(self):
        self.sprite_sheet = pygame.image.load("./sprites/spritesheet.png")
        self.sprite_sheet_width = self.sprite_sheet.get_rect().width / self.SPRITE_RESOLUTION
        self.sprite_sheet_height = self.sprite_sheet.get_rect().height / self.SPRITE_RESOLUTION
        self.screen = pygame.display.set_mode((1280, 720))
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (self.sprite_sheet_width * self.SPRITE_RESOLUTION * self.DEFAULT_SCALE, self.sprite_sheet_height * self.SPRITE_RESOLUTION * self.DEFAULT_SCALE))

    def draw_sprite(self, index, x, y):
        rect = ((index % self.sprite_sheet_width) * self.SPRITE_RESOLUTION * self.DEFAULT_SCALE, 
                math.floor(index / self.sprite_sheet_width) * self.SPRITE_RESOLUTION * self.DEFAULT_SCALE, self.SPRITE_RESOLUTION * self.DEFAULT_SCALE, self.SPRITE_RESOLUTION * self.DEFAULT_SCALE)
        self.screen.blit(self.sprite_sheet, (x * self.DEFAULT_SCALE, y * self.DEFAULT_SCALE),rect)

    def update_screen(self):
        self.screen.fill((0, 0, 0))
