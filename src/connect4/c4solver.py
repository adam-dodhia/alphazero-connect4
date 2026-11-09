"""Print the solver's evaluation of each column for a Connect 4 position.

Usage: python c4solver.py [MOVES]

MOVES is the 1-indexed column history, e.g. "4453". Omit it for the empty board.

Scores are from the point of view of the player to move: positive wins, negative
loses, 0 draws. The magnitude is 1 + the number of stones the winner still has
unplayed when the game ends, so a larger magnitude means a faster win.
"""
import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOLVER = HERE / "c4solver.exe"
BOOK = HERE / "7x6.book"

NUM_COLUMNS = 7
FULL_COLUMN = -1000  # the solver's marker for a column that can't be played


def evaluate(moves: str) -> list[int | None]:
    """Return one score per column, left to right, with None for full columns.

    Raises ValueError if the solver rejects the position, which happens for an
    illegal move or a history that continues past the end of the game.
    """
    result = subprocess.run(
        [SOLVER, "-a", "-b", BOOK],
        input=moves + "\n", capture_output=True, text=True,
    )
    lines = result.stdout.strip().splitlines()
    try:
        scores = [int(token) for token in lines[-1].split()[-NUM_COLUMNS:]]
    except (IndexError, ValueError):
        scores = []
    if len(scores) != NUM_COLUMNS:
        detail = (result.stderr.strip() or result.stdout.strip()).splitlines()
        reason = detail[-1] if detail else f"solver exited with {result.returncode}"
        raise ValueError(f"Invalid position {moves!r}: {reason}")
    return [None if score == FULL_COLUMN else score for score in scores]


def evaluate_history(move_history: list[int]) -> list[int | None]:
    """Same as evaluate(), for a game's zero-indexed move_history."""
    return evaluate("".join(str(column + 1) for column in move_history))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print the solver's evaluation of each column."
    )
    parser.add_argument(
        "moves", nargs="?", default="",
        help='1-indexed column history, e.g. "4453" (default: empty board)',
    )
    args = parser.parse_args()

    try:
        scores = evaluate(args.moves)
    except ValueError as error:
        sys.exit(str(error))

    print("column  score")
    for column, score in enumerate(scores, start=1):
        print(f"{column:>6}  {'full' if score is None else score:>5}")

    legal = [score for score in scores if score is not None]
    if legal:
        best = [str(c) for c, s in enumerate(scores, start=1) if s == max(legal)]
        print(f"best column: {', '.join(best)}")
    else:
        print("best column: none (board is full)")


if __name__ == "__main__":
    main()
