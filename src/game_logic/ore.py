class Ore:
    def __init__(self):
        self.sprite = 0
        self.color = (0, 0, 0)
        self.value = 0
        self.toughness_multiplier = 0
        self.exists = False
        self.is_coal = False
        self.rarity = 0

    def set_ore(self, sprite, color, value, toughness_multiplier, exists, is_coal, rarity):
        self.sprite = sprite
        self.color = color
        self.value = value
        self.toughness_multiplier = toughness_multiplier
        self.exists = exists
        self.is_coal = is_coal
        self.rarity = rarity