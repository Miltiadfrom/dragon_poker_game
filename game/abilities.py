def thief_ability(game, player):
    """Вор: украдите 7 золота из банка"""
    stolen = min(7, game.bank.gold)
    game.bank.gold -= stolen
    player.hoard += stolen
    print(f"{player.name} украл {stolen} золота из банка!")

def golden_dragon_ability(game, player):
    """Золотой Дракон: тянет карту за каждого доброго дракона в стае"""
    good_dragons = [card for card in player.flight if card.type == "добро"]
    count = len(good_dragons)
    player.draw_cards(game.deck, count)
    print(f"{player.name} получил {count} карт за добрых драконов")

def archmage_ability(game, player):
    """Архимаг: копирует способность любой карты ставки"""
    if game.current_ante:
        chosen = game.current_ante[0]
        print(f"{player.name} копирует способность: {chosen.name}")
        if chosen.ability:
            chosen.ability(game, player)
    else:
        print(f"{player.name} не нашёл карт для копирования")

def dragon_lord_ability(game, player):
    """Драколич: копирует способность любого злого дракона"""
    evil_dragons = [card for card in player.flight if card.type == "зло"]
    if evil_dragons:
        chosen = evil_dragons[0]
        print(f"{player.name} копирует способность: {chosen.name}")
        if chosen.ability:
            chosen.ability(game, player)
    else:
        print(f"{player.name} не нашёл злых драконов для копирования")

def black_dragon_ability(game, player):
    """Чёрный Дракон: украдите 2 золота у другого игрока"""
    if len(game.players) <= 1:
        return
    targets = [p for p in game.players if p != player]
    target = targets[0]  # Простой выбор: первый другой игрок
    stolen = min(2, target.hoard)
    target.hoard -= stolen
    player.hoard += stolen
    print(f"{player.name} украл {stolen} золота у {target.name}")

def blue_dragon_ability(game, player):
    """Синий Дракон: сбросьте карту из руки, чтобы украсть 1 золото"""
    if not player.hand:
        return
    discarded = player.hand.pop(0)
    game.deck.discard_pile.append(discarded)
    stolen = min(1, game.bank.gold)
    game.bank.gold -= stolen
    player.hoard += stolen
    print(f"{player.name} сбросил карту и украл 1 золото")

def brass_dragon_ability(game, player):
    """Латунный Дракон: получите 1 золото за каждую карту в руке"""
    gold = len(player.hand)
    player.hoard += gold
    game.bank.gold -= gold
    print(f"{player.name} получил {gold} золота за карты в руке")

def bronze_dragon_ability(game, player):
    """Бронзовый Дракон: тянет карту за каждого игрока со стаей сильнее вашей"""
    stronger_players = [p for p in game.players if p != player and sum(c.strength for c in p.flight) > sum(c.strength for c in player.flight)]
    count = len(stronger_players)
    player.draw_cards(game.deck, count)
    print(f"{player.name} получил {count} карт за сильных игроков")

def copper_dragon_ability(game, player):
    """Медный Дракон: тянет карту за каждую карту ставки"""
    count = len(game.current_ante)
    player.draw_cards(game.deck, count)
    print(f"{player.name} получил {count} карт за ставки")

def green_dragon_ability(game, player):
    """Зелёный Дракон: противник слева отдаёт вам злого дракона"""
    left_player = game.players[(game.players.index(player) + 1) % len(game.players)]
    evil_dragons = [c for c in left_player.hand if c.type == "зло"]
    if evil_dragons:
        chosen = evil_dragons[0]
        left_player.hand.remove(chosen)
        player.hand.append(chosen)
        print(f"{left_player.name} отдал {chosen.name} игроку {player.name}")

def red_dragon_ability(game, player):
    """Красный Дракон: получите 1 золото за каждый злой дракон в стае"""
    evil_dragons = [c for c in player.flight if c.type == "зло"]
    gold = len(evil_dragons)
    player.hoard += gold
    game.bank.gold -= gold
    print(f"{player.name} получил {gold} золота за злых драконов")

def silver_dragon_ability(game, player):
    """Серебряный Дракон: каждый игрок с добрым драконом в стае тянет карту"""
    for p in game.players:
        good_dragons = [c for c in p.flight if c.type == "добро"]
        if good_dragons and len(p.hand) < 10:
            p.draw_cards(game.deck, 1)

def dragon_god_ability(game, player):
    """Бог Драконов: игрок с самой слабой стаей теряет 5 золота"""
    weakest = min(game.players, key=lambda p: sum(c.strength for c in p.flight))
    lost = min(5, weakest.hoard)
    weakest.hoard -= lost
    game.bank.gold += lost
    print(f"{weakest.name} потерял {lost} золота из-за Бога Драконов")

def fool_ability(game, player):
    """Дурак: получите карту за каждого игрока со стаей сильнее вашей"""
    stronger_players = [p for p in game.players if p != player and sum(c.strength for c in p.flight) > sum(c.strength for c in player.flight)]
    count = len(stronger_players)
    if count > 0:
        player.draw_cards(game.deck, count)
        print(f"{player.name} получил {count} карт за сильных игроков")
    else:
        # Заплатите 1 золото в банк
        paid = min(1, player.hoard)
        player.hoard -= paid
        game.bank.gold += paid
        print(f"{player.name} заплатил 1 золото в банк")

def dragon_killer_ability(game, player):
    """Убийца Драконов: уничтожьте дракона из стаи другого игрока"""
    if len(game.players) <= 1:
        return
    targets = [p for p in game.players if p != player]
    target = targets[0]
    dragons = [c for c in target.flight if c.dragon_color]
    if dragons:
        destroyed = dragons[0]
        target.flight.remove(destroyed)
        game.deck.discard_pile.append(destroyed)
        print(f"{player.name} уничтожил {destroyed.name} у {target.name}")

def druid_ability(game, player):
    """Друид: тянет карту за каждого дракона в стае"""
    dragons = [c for c in player.flight if c.dragon_color]
    count = len(dragons)
    player.draw_cards(game.deck, count)
    print(f"{player.name} получил {count} карт за драконов")

def priest_ability(game, player):
    """Жрец: получите 2 золота за каждую карту ставки"""
    gold = len(game.current_ante) * 2
    player.hoard += gold
    game.bank.gold -= gold
    print(f"{player.name} получил {gold} золота за ставки")

def princess_ability(game, player):
    """Принцесса: получите 3 золота за каждую карту в руке"""
    gold = len(player.hand) * 3
    player.hoard += gold
    game.bank.gold -= gold
    print(f"{player.name} получил {gold} золота за карты в руке")

def white_dragon_ability(game, player):
    """Белый Дракон: украдите 1 золото у всех игроков"""
    for p in game.players:
        if p != player and p.hoard > 0:
            stolen = min(1, p.hoard)
            p.hoard -= stolen
            player.hoard += stolen
            print(f"{player.name} украл {stolen} золота у {p.name}")

def joker_ability(game, player):
    """Джокер: сбросьте карту из руки, чтобы получить 2 золота"""
    if not player.hand:
        return
    discarded = player.hand.pop(0)
    game.deck.discard_pile.append(discarded)
    gold = 2
    player.hoard += gold
    game.bank.gold -= gold
    print(f"{player.name} сбросил карту и получил 2 золота")

def quick_hands_ability(game, player):
    """Ловкость Рук: после кражи золота украдите ещё 1 золото, если банк >= 2"""
    if game.bank.gold >= 2:
        stolen = min(1, game.bank.gold)
        game.bank.gold -= stolen
        player.hoard += stolen
        print(f"{player.name} украл дополнительное {stolen} золота благодаря Ловкости Рук")