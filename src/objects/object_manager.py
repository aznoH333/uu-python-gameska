from sprites.drawing_manager import DrawingManager
from game_logic.world_manager import WorldManager



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
        self.world.obj_man = self # dependency circle of shame


    def add_object(self, object):
        self.objects.append(object)

    def update(self):
        for object in self.objects:
            #update
            object.update(self.world.get_depth())
            #draw
            self.drawing_man.draw_sprite(object.sprite_index, object.x + object.x_offset, object.y + object.y_offset - self.world.get_depth(), object.color)
        
            if object.wants_to_be_alive == False:
                self.objects.remove(object)