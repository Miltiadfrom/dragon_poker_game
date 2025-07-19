class Card:
    def __init__(self, name, strength, type, dragon_color=None, ability=None):
        self.name = name
        self.strength = strength
        self.type = type  # "добро", "зло", "смертный"
        self.dragon_color = dragon_color  # цвет дракона, если это дракон
        self.ability = ability  # функция, принимающая (game, player)

    def use(self, game, player):
        if self.ability:
            self.ability(game, player)

    def __repr__(self):
        return f"{self.name}({self.strength})"