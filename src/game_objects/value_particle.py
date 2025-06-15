from engine.engine import Engine
from objects.base_object import BaseObject
from sprites.drawing_manager import DrawingManager


class ValueParticle(BaseObject):
    def __init__(self, x, y, color, text):
        super().__init__(x, y, 1, 0, 0, 0, 0, (0, 0, 0, 0))
        self.text_color = color
        self.text = text
        self.life_time = 120
        self.engine = Engine.get_instance()
        self.drawing_man = DrawingManager.get_instance()
    
    def update(self, depth):
        self.y -= 0.2 * self.engine.get_delta()
        self.life_time -= self.engine.get_delta()

        if self.life_time < 0:
            self.wants_to_be_alive = False

        self.drawing_man.draw_text(self.text, self.x, self.y - depth, self.text_color)