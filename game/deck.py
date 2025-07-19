import random

class Deck:
    def __init__(self, cards):
        self.cards = cards.copy()
        random.shuffle(self.cards)
        self.discard_pile = []

    def draw(self):
        if not self.cards:
            self.reshuffle_discard()
        return self.cards.pop()

    def reshuffle_discard(self):
        if self.discard_pile:
            self.cards = self.discard_pile.copy()
            self.discard_pile.clear()
            random.shuffle(self.cards)

    def discard(self, card):
        self.discard_pile.append(card)