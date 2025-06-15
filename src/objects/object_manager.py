from engine.utils import box_collision
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
        for i in range(0, len(self.objects)):
            object = self.objects[i]
            
            #draw
            self.drawing_man.draw_sprite(object.sprite_index, object.x + object.x_offset, object.y + object.y_offset - self.world.get_depth(), object.color)
        
            #update
            object.update(self.world.get_depth())

            # collisions
            for j in range(0, len(self.objects)):
                other = self.objects[j]
                if i != j and box_collision(object.x, object.y, object.width, object.height, other.x, other.y, other.width, other.height):
                    object.on_collide(other)
            

            
        #deleting
        for object in self.objects:
            if object.wants_to_be_alive == False:
                self.objects.remove(object)