from sprites.drawing_manager import DrawingManager
from world.world_manager import WorldManager



class ObjectManager:
    instance = None
    def get_instance():
        if ObjectManager.instance == None:
            ObjectManager.instance = ObjectManager()
        return ObjectManager.instance
    
    def __init__(self):
        self.objects = []
        self.drawing_man = DrawingManager.get_instance()
        self.world = WorldManager.get_instance()


    def add_object(self, object):
        self.objects.append(object)

    def update(self):
        for object in self.objects:
            #update
            object.update()
            #draw
            self.drawing_man.draw_sprite(object.sprite_index, object.x + object.x_offset, object.y + object.y_offset - self.world.get_depth())