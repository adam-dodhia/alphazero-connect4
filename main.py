"""Command line interface for Connect 4."""

from core import COLUMNS, Connect4Game
from players import HumanPlayer, Player
from random_agent import RandomModel

HIGHLIGHT = "\033[47m\033[30m"  # white background, black foreground
RESET = "\033[0m"


def print_board(game: Connect4Game) -> None:
    winning_cells = set(game.winning_cells or [])

    print()
    for row_index, row in enumerate(game.board):
        cells = []
        for column_index, cell in enumerate(row):
            if (row_index, column_index) in winning_cells:
                cells.append(f"{HIGHLIGHT}{cell}{RESET}")
            else:
                cells.append(cell)
        print(" ".join(cells))
    print(" ".join(str(column + 1) for column in range(COLUMNS)))
    print()


def play(players: dict[str, Player]) -> None:
    game = Connect4Game()
    print_board(game)

    while not game.game_over:
        player = players[game.current_player]
        column = player.get_move(game)
        game.drop_piece(column)
        print_board(game)

    if game.winner:
        print(f"{players[game.winner].name} wins!")
    else:
        print("It's a draw!")


def main() -> None:
    players: dict[str, Player] = {
        "X": HumanPlayer("Player 1", "X"),
        "O": RandomModel("Player 2", "O"),
    }
    play(players)


if __name__ == "__main__":
    main()