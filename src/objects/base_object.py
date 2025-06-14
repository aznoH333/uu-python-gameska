class BaseObject:

    def __init__(self, x, y, sprite_index, width, height, x_offset = 0, y_offset = 0, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.sprite_index = sprite_index
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.color = color
        self.wants_to_be_alive = True



    def update():
        print("undefine update")

