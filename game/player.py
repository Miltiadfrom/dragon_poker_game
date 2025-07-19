class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.flight = []
        self.hoard = 50
        self.debt = 0  # Начальный долг

    def draw_cards(self, deck, count=2):
        while len(self.hand) < 10 and count > 0:
            if not deck.cards:
                if deck.discard_pile:
                    deck.reshuffle_discard()
                else:
                    break  # Нет карт для тяги
            self.hand.append(deck.draw())
            count -= 1

    def pay_gold(self, amount):
        """Платит указанное количество золота, сначала погашает долги"""
        paid = 0
        if self.debt > 0:
            debt_payment = min(amount, self.debt)
            self.debt -= debt_payment
            paid += debt_payment
            amount -= debt_payment
        if amount > 0:
            gold_payment = min(amount, self.hoard)
            self.hoard -= gold_payment
            paid += gold_payment
        return paid

    def add_debt(self, amount):
        """Добавляет долг"""
        self.debt += amount

    def discard_card(self, card):
        self.hand.remove(card)

    def play_card(self, card, game):
        self.flight.append(card)
        self.hand.remove(card)
        card.use(game, self)