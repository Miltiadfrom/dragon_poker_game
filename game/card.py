class Card:
    def __init__(self, name, strength, type, dragon_color=None, ability=None):
        self.name = name
        self.strength = strength
        self.type = type  # Изменено с card_type на type
        self.dragon_color = dragon_color
        self.ability = ability

    def use(self, game, player):
        if self.ability:
            self.ability(game, player)

    def __repr__(self):
        return f"{self.name}({self.strength})"