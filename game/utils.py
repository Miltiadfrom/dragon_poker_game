import json
from game.card import Card

def load_cards_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cards = []
    for item in data:
        # Явно указываем значения по умолчанию
        card = Card(
            name=item.get("name", "Неизвестная карта"),
            strength=item.get("strength", 0),
            type=item.get("type", "смертный"),
            dragon_color=item.get("dragon_color", None),
            ability=item.get("ability", None)
        )
        cards.append(card)
    return cards