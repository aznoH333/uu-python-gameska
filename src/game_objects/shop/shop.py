import pygame
from engine.engine import Engine
from game_logic.game_stats import GameStats
from game_objects.shop.shop_item import ShopItem
from game_objects.shop.shop_item_type import ShopItemType
from objects.base_object import BaseObject
from sprites.drawing_manager import DrawingManager


class Shop(BaseObject):
    INTERACTION_COOLDOWN = 10
    
    def __init__(self, x, y):
        super().__init__(x, y, 27, 32, 32, 0, 0)
        self.active = True
        self.open = False
        self.items = []
        self.index = 0

        self.stats = GameStats.get_instance()
        self.items.append(ShopItem("Odejít", 0, ShopItemType.EXIT))
        self.items.append(ShopItem("Palivo", 200, ShopItemType.FUEL))
        self.drawing_man = DrawingManager.get_instance()
        self.engine = Engine.get_instance()
        self.interaction_cooldown = 30
        # generate items
        for i in range(0, 2):
            self.generate_random_item()


        
    
    def update(self, depth):
        #kill
        if self.y - depth < -64:
            self.wants_to_be_alive = False

        if self.active == False:
            self.sprite_index = 28


        # display menu
        if self.open:
            # render items
            for i in range(0, len(self.items)):
                item = self.items[i]
                color = (255, 255, 255)
                if i == self.index:
                    color = (255, 255, 0)

                price = ""
                if item.price != 0:
                    price = f"{item.price}$"
                self.drawing_man.draw_text(f"{item.text}    {price}", 30, 180 + (i * 40), color)

            
            # index moving
            if self.interaction_cooldown <= 0:
                if self.engine.is_key_down(pygame.K_UP):
                    self.index -= 1
                    self.interaction_cooldown = self.INTERACTION_COOLDOWN
                elif self.engine.is_key_down(pygame.K_DOWN):
                    self.index += 1
                    self.interaction_cooldown = self.INTERACTION_COOLDOWN
                elif self.engine.is_key_down(pygame.K_RIGHT):
                    self.pick_upgrade(self.index)
                    self.interaction_cooldown = self.INTERACTION_COOLDOWN

            else:
                self.interaction_cooldown -= self.engine.get_delta()

            
            # fix index
            if self.index < 0:
                self.index = len(self.items) - 1
            elif self.index > len(self.items) - 1:
                self.index = 0


            


    def generate_random_item(self):
        self.items.append(ShopItem("Rychlost těžení", 200, ShopItemType.DRILL_UPGRADE)) # TODO : more upgrades

    def pick_upgrade(self, index):
        upgrade = self.items[index]
        match(upgrade.type):
            case ShopItemType.EXIT:
                print("leavuju")
                self.open = False
                self.active = False
            case ShopItemType.FUEL:
                self.stats.add_fuel(999999999)
            case ShopItemType.DRILL_UPGRADE:
                print("TODO this")
        
        del self.items[index]


    def interact(self):
        self.open = True