from connect4.players import Player
from connect4.c4solver import evaluate

class SolverModel(Player):
    def get_move(self, game) -> int:
        scores = evaluate("".join(str(column + 1) for column in game.move_history))
        best_score = max(score for score in scores if score is not None)
        for column, score in enumerate(scores):
            if score == best_score:
                return column
        