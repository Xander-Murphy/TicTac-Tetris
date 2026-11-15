"""
Helpers for writing board tests as plain number grids.

Board stores Cell objects, which are awkward to compare directly. These
helpers let a test describe a board as rows of ints (0 = empty, anything
else = a filled cell with that tile color), the same format the mission
layouts in mission_data.py use.
"""

from elements.gameLogic.board import Board


def board_from_rows(rows):
    """Build a Board whose cells match `rows` (lists of ints)."""
    return Board(len(rows), len(rows[0]), rows)


def grid_values(board):
    """Read a Board back as rows of ints: tile color if filled, else 0."""
    return [
        [cell.tileTexture if board.is_cell_occupied(cell) else 0 for cell in row]
        for row in board.grid
    ]


def is_filled(board, row, col):
    return board.is_cell_occupied(board.get_cell(row, col))
