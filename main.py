from game.game import Game
from game.player import Player

if __name__ == "__main__":
    players = [Player("Игрок 1"), Player("Игрок 2")]
    game = Game(players)
    game.start_game()

    while not game.check_game_end():
        game.ante_phase()
        while not game.is_gambit_over():
            if all(len(p.hand) == 0 for p in players):
                print("=== Гамбит окончен: все игроки без карт ===")
                break
            game.round_phase()
        game.end_gambit()

    winner = game.get_winner()
    print(f"Игра окончена! Победитель: {winner.name} с {winner.hoard} золотыми")