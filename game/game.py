from game.deck import Deck  # Импортируем класс Deck
from game.bank import Bank
from game.utils import load_cards_from_json

class Game:
    def __init__(self, players):
        self.players = players
        self.bank = Bank()
        self.deck = Deck(load_cards_from_json("data/cards.json"))  # Теперь Deck доступен
        self.leader = None
        self.current_ante = []

    def start_game(self):
        if len(self.players) < 2:
            raise ValueError("Минимум 2 игрока требуется для игры")
        for player in self.players:
            player.draw_cards(self.deck, 6)

    def ante_phase(self):
        print("=== Фаза ставки ===")
        bets = []
        for player in self.players:
            card = player.hand[0]  # упрощённый выбор
            bets.append((player, card))
            print(f"{player.name} ставит {card}")
            player.hand.remove(card)

        # определяем лидера
        bets.sort(key=lambda x: x[1].strength, reverse=True)
        strongest = bets[0][1].strength
        print(f"Максимальная ставка: {strongest}")
        self.leader = bets[0][0]

        # пополняем банк
        for player in self.players:
            amount = min(strongest, player.hoard)
            player.hoard -= amount
            self.bank.add_gold(amount)

        self.current_ante = [card for player, card in bets]

    def round_phase(self):
        print("=== Раунд ===")
        order = self.get_players_in_order(self.leader)
        for player in order:
            if not player.hand:
                print(f"{player.name} не может сделать ход — нет карт в руке!")
                continue
            card = player.hand[0]
            print(f"{player.name} играет карту: {card}")
            player.play_card(card, self)

    def get_players_in_order(self, leader):
        idx = self.players.index(leader)
        return self.players[idx:] + self.players[:idx]

    def is_gambit_over(self):
        return self.bank.gold == 0 or len(self.current_ante) >= 3

    def end_gambit(self):
        print("=== Гамбит окончен ===")
        self.check_special_flights()  # Проверяем специальные стаи

        winner = max(self.players, key=lambda p: sum(c.strength for c in p.flight))
        print(f"{winner.name} выигрывает банк из {self.bank.gold} золотых!")
        winner.hoard += self.bank.take_gold(self.bank.gold)

        # Победитель гамбита игнорирует долги
        for player in self.players:
            if player == winner:
                player.debt = 0
            else:
                # Погашение долгов
                if player.debt > 0:
                    paid = player.pay_gold(player.debt)
                    print(f"{player.name} погасил {paid} из {player.debt} долгов")
                    player.debt -= paid

        # Перемещаем карты из стаи и ставок в discard
        for player in self.players:
            for card in player.flight:
                self.deck.discard_pile.append(card)
            player.flight.clear()

        for card in self.current_ante:
            self.deck.discard_pile.append(card)
        self.current_ante = []

        # Перемешиваем discard, если колода пуста
        if not self.deck.cards and self.deck.discard_pile:
            self.deck.reshuffle_discard()

        # Игроки тянут по 2 карты
        for player in self.players:
            player.draw_cards(self.deck, 2)

    def check_game_end(self):
        return any(p.hoard <= 0 for p in self.players)

    def get_winner(self):
        return max(self.players, key=lambda p: p.hoard)

    def check_special_flights(self):
        """Проверяет наличие специальных стай: цвет и сила"""
        for player in self.players:
            dragons = [card for card in player.flight if card.dragon_color]
            if not dragons:
                continue

            # Проверка стаи одного цвета
            color_counts = {}
            for d in dragons:
                color_counts[d.dragon_color] = color_counts.get(d.dragon_color, 0) + 1
            for color, count in color_counts.items():
                if count >= 3:
                    # Игрок получает награду за стаю одного цвета
                    sorted_dragons = sorted(dragons, key=lambda x: x.strength, reverse=True)
                    if len(sorted_dragons) >= 2:
                        reward = sorted_dragons[1].strength
                    else:
                        reward = 0
                    print(
                        f"{player.name} завершил стаю одного цвета ({color}), получает {reward} золота за каждого противника")
                    for p in self.players:
                        if p != player:
                            paid = p.pay_gold(reward)
                            player.hoard += paid
                    break

            # Проверка силовой стаи
            strength_counts = {}
            for d in dragons:
                strength_counts[d.strength] = strength_counts.get(d.strength, 0) + 1
            for strength, count in strength_counts.items():
                if count >= 3:
                    print(
                        f"{player.name} завершил силовую стаю (сила {strength}), получает 5 золота за каждого противника")
                    for p in self.players:
                        if p != player:
                            paid = p.pay_gold(5)
                            player.hoard += paid
                    break

            # Проверка силы
            for strength, count in strength_counts.items():
                if count >= 3:
                    print(f"{player.name} создал стаю одной силы: {strength}")
                    player.hoard += 5  # Пример вознаграждения
                    break

    def buy_cards(self, player):
        """Игрок покупает карты: сбрасывает верхнюю карту и платит силу карты в банк"""
        if not player.hand:
            # Сбрасываем верхнюю карту из колоды
            if not self.deck.cards and self.deck.discard_pile:
                self.deck.reshuffle_discard()
            if self.deck.cards:
                discarded = self.deck.draw()
                self.deck.discard_pile.append(discarded)
                print(f"{player.name} сбросил {discarded.name} при покупке карт")
            # Платим силу карты в банк
            cost = discarded.strength if discarded else 1
            paid = player.pay_gold(cost)
            self.bank.add_gold(paid)
            # Тянем карты до 4
            player.draw_cards(self.deck, 4)