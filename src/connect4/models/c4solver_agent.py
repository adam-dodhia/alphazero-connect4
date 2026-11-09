import random

from connect4.players import Player
from connect4.c4solver import evaluate_history


class SolverModel(Player):
    def __init__(self, name: str, symbol: str, *, seed: int | None = None) -> None:
        super().__init__(name, symbol)
        self.rng = random.Random(seed)

    def get_move(self, game) -> int:
        """Return a random choice among the columns the solver scores highest."""
        scores = evaluate_history(game.move_history)
        best_score = max(score for score in scores if score is not None)
        return self.rng.choice([column for column, score in enumerate(scores) if score == best_score])
