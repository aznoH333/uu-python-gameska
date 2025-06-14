from sprites.sprite_manager import SpriteManager
from world.world_manager import WorldManager



class ObjectManager:
    instance = None
    def get_instance():
        if ObjectManager.instance == None:
            ObjectManager.instance = ObjectManager()
        return ObjectManager.instance
    
    def __init__(self):
        self.objects = []
        self.sprite_man = SpriteManager.get_instance()
        self.world = WorldManager.get_instance()


    def add_object(self, object):
        self.objects.append(object)

    def update(self):
        for object in self.objects:
            #update
            object.update()
            #draw
            self.sprite_man.draw_sprite(object.sprite_index, object.x + object.x_offset, object.y + object.y_offset - self.world.get_depth())