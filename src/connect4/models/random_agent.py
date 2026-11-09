from connect4.players import Player
import random

class RandomModel(Player):
    def get_move(self, game) -> int:
        valid_moves = game.valid_moves()
        chosen_move = random.sample(valid_moves, 1)[0]
        return chosen_move