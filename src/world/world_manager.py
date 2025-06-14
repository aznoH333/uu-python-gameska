class WorldManager:
    instance = None
    def get_instance():
        if WorldManager.instance == None:
            WorldManager.instance = WorldManager()

        return WorldManager.instance
    


    def update(self):
        pass