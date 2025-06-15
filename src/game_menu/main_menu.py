import pygame
import pygame.freetype
from pygame.rect import Rect
from pygame.sprite import Sprite

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

def create_surface(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", bold=True)
    surface, _ =font.render(text=text, fgcolor=text_rgb, bg_color=bg_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):

    def __init__(self, center_pos, text, font_size, bg_rgb, text_rgb):
        self.mouse_over = False

        default_image = create_surface(text, font_size, text_rgb, bg_rgb)

        highlight_image = create_surface(text, font_size*1.2, text_rgb, bg_rgb)

        self.images = [default_image, highlight_image]
        self.rects = (default_image.get_rect(center=center_pos), highlight_image.get_rect(center=center_pos))


    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


    def main_menu(self):
       screen.fill(BLUE)

       uielement.update(pygame.mouse.get_pos())
       uielement.draw(screen)
       pygame.display.flip()

