import math
import random
import pygame
from engine.engine import Engine
from game_logic.game_stats import GameStats
from game_objects.shop.shop_item import ShopItem
from game_objects.shop.shop_item_type import ShopItemType
from objects.base_object import BaseObject
from sprites.drawing_manager import DrawingManager


class Shop(BaseObject):
    INTERACTION_COOLDOWN = 10
    
    def __init__(self, x, y, depth):
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
            self.generate_random_item(depth)


        
    
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


            


    def generate_random_item(self, depth):
        price = math.floor((200 + (math.pow(1.5 - 0.5, 2) * 600)) + (depth)) * random.randint(45, 55)

        index = random.randint(2, 4)
        type = ShopItemType(index)
        text = ""

        match (type):
            case ShopItemType.DRILL_UPGRADE:
                price *= 1.2
                text = "Rychlost těžení"
            case ShopItemType.FUEL_CAPACITY:
                price *= 0.7
                text = "Kapacita paliva"
            case ShopItemType.FUEL_EFFICIENCY:
                text = "Effektivita motoru"


        self.items.append(ShopItem(text, math.floor(price), type))

    def pick_upgrade(self, index):
        upgrade = self.items[index]
        match(upgrade.type):
            case ShopItemType.EXIT:
                self.open = False
                self.active = False
            case ShopItemType.FUEL:
                self.stats.add_fuel(999999999)
            case ShopItemType.DRILL_UPGRADE:
                self.stats.mining_power += 10
            case ShopItemType.FUEL_CAPACITY:
                self.stats.max_fuel += 10
            case ShopItemType.FUEL_EFFICIENCY:
                self.stats.fuel_efficiency += 1
        
        del self.items[index]


    def interact(self):
        self.open = True