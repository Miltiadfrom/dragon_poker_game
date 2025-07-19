class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.flight = []
        self.hoard = 50
        self.debt = 0

    def draw_cards(self, deck, count=2):
        while len(self.hand) < 10 and count > 0:
            if not deck.cards and not deck.discard_pile:
                # Нет карт для тяги
                return
            if not deck.cards:
                deck.reshuffle_discard()
            self.hand.append(deck.draw())
            count -= 1

    def discard_card(self, card):
        self.hand.remove(card)

    def play_card(self, card, game):
        self.flight.append(card)
        self.hand.remove(card)
        card.use(game, self)