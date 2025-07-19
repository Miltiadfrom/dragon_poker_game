class Bank:
    def __init__(self):
        self.gold = 0

    def add_gold(self, amount):
        self.gold += amount

    def take_gold(self, amount):
        taken = min(amount, self.gold)
        self.gold -= taken
        return taken

    def __repr__(self):
        return f"Bank({self.gold})"