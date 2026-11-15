"""
Unit tests for board.py.

Board has no pygame dependency, so these tests need no display and run
fast. Where a test needs a "piece", we use the real Piece class rather
than a hand-rolled fake - Board.intersects()/lock_piece() only need an
object with .x, .y, .image() and .color, which Piece already is.

Boards are described as rows of ints via grid_helpers (0 = empty,
anything else = filled with that tile color).
"""

import pytest

from elements.gameLogic.board import Board
from elements.gameLogic.cell import Cell, CellStatus
from elements.gameLogic.piece import Piece
from grid_helpers import board_from_rows, grid_values, is_filled


# A simple 2x2 square piece (Type 6, rotation 0) is used throughout as
# a predictable shape: image() == [1, 2, 5, 6], i.e. a 2-row, 2-col
# block occupying (row+0,col+1), (row+0,col+2), (row+1,col+1), (row+1,col+2).
def square_piece(x, y):
    return Piece(piece_type=6, x=x, y=y)


# ---------------------------------------------------------------------
# construction
# ---------------------------------------------------------------------

def test_empty_board_has_correct_dimensions_and_all_empty_cells():
    board = Board(height=5, width=4)
    assert board.height == 5
    assert board.width == 4
    assert len(board.grid) == 5
    assert all(len(row) == 4 for row in board.grid)
    assert grid_values(board) == [[0] * 4 for _ in range(5)]


def test_every_cell_knows_its_own_position():
    board = Board(height=3, width=2)
    for row_index, row in enumerate(board.grid):
        for col_index, cell in enumerate(row):
            assert (cell.row, cell.column) == (row_index, col_index)


def test_initial_grid_fills_cells_with_their_tile_color():
    rows = [
        [0, 3],
        [7, 0],
    ]
    board = board_from_rows(rows)
    assert grid_values(board) == rows
    assert board.get_cell(0, 1).status is CellStatus.FILLED
    assert board.get_cell(0, 0).status is CellStatus.EMPTY


def test_board_with_initial_grid_copies_rather_than_aliases():
    """
    Mission mode passes in a shared MISSION_FIELD constant. If Board
    stored that list by reference instead of copying it, playing one
    mission-mode game would permanently mutate MISSION_FIELD for every
    future game. This guards against that.
    """
    original = [[0, 0], [0, 0]]
    board = Board(height=2, width=2, initial_grid=original)
    board.lock_piece(square_piece(x=-1, y=0))  # fills the whole 2x2 board
    assert original == [[0, 0], [0, 0]]  # original untouched


def test_two_boards_from_the_same_layout_do_not_share_cells():
    rows = [[0, 1], [1, 1]]
    first, second = board_from_rows(rows), board_from_rows(rows)
    first.get_cell(0, 0).status = CellStatus.FILLED
    assert not is_filled(second, 0, 0)


def test_is_cell_occupied():
    board = Board(height=2, width=2)
    cell = board.get_cell(0, 0)
    assert board.is_cell_occupied(cell) is False
    cell.status = CellStatus.FILLED
    assert board.is_cell_occupied(cell) is True


def test_preview_cells_do_not_count_as_occupied():
    board = Board(height=1, width=1)
    cell = board.get_cell(0, 0)
    cell.status = CellStatus.PREVIEW
    assert board.is_cell_occupied(cell) is False


def test_get_cell_returns_the_cell_at_row_and_column():
    board = Board(height=3, width=3)
    cell = board.get_cell(2, 1)
    assert isinstance(cell, Cell)
    assert cell is board.grid[2][1]


@pytest.mark.parametrize("rows, row, expected", [
    ([[0, 0, 0], [0, 0, 0]], 1, True),
    ([[0, 0, 0], [0, 5, 0]], 1, False),
    ([[4, 4, 4], [0, 0, 0]], 1, True),  # other rows don't matter
])
def test_is_row_empty(rows, row, expected):
    assert board_from_rows(rows).is_row_empty(row) is expected


# ---------------------------------------------------------------------
# intersects()
# ---------------------------------------------------------------------

def test_intersects_false_when_space_is_clear():
    board = Board(height=10, width=10)
    piece = square_piece(x=0, y=0)
    assert board.intersects(piece) is False


def test_intersects_true_past_right_wall():
    board = Board(height=10, width=3)  # columns 0,1,2 only
    piece = square_piece(x=2, y=0)  # square needs columns 1 and 2 -> col 2+2=4, out of range
    assert board.intersects(piece) is True


def test_intersects_true_past_left_wall():
    board = Board(height=10, width=10)
    piece = square_piece(x=-2, y=0)  # pushes column 1 of the shape to -1
    assert board.intersects(piece) is True


def test_intersects_true_past_bottom():
    board = Board(height=2, width=10)  # rows 0,1 only
    piece = square_piece(x=0, y=1)  # square needs row 1+1=2, out of range
    assert board.intersects(piece) is True


def test_intersects_true_when_overlapping_filled_cell():
    board = Board(height=10, width=10)
    board.get_cell(1, 2).status = CellStatus.FILLED  # a cell the square would land on
    piece = square_piece(x=0, y=0)
    assert board.intersects(piece) is True


# ---------------------------------------------------------------------
# lock_piece()
# ---------------------------------------------------------------------

def test_lock_piece_writes_the_pieces_color_into_the_grid():
    board = Board(height=3, width=4)
    piece = square_piece(x=0, y=0)
    board.lock_piece(piece)
    c = piece.color
    assert grid_values(board) == [
        [0, c, c, 0],
        [0, c, c, 0],
        [0, 0, 0, 0],
    ]


# ---------------------------------------------------------------------
# clear_full_lines()
# ---------------------------------------------------------------------

def test_clear_full_lines_clears_a_full_row_and_returns_count():
    board = board_from_rows([
        [0, 0, 0],
        [1, 0, 0],
        [1, 2, 3],  # full row
        [0, 0, 0],
    ])
    lines_cleared = board.clear_full_lines()
    assert lines_cleared == 1
    assert grid_values(board) == [
        [0, 0, 0],
        [0, 0, 0],
        [1, 0, 0],  # row 1 shifted down into row 2
        [0, 0, 0],
    ]


def test_clear_full_lines_does_nothing_when_no_row_is_full():
    rows = [
        [0, 0, 0],
        [7, 7, 0],  # one empty cell - not full
        [1, 0, 0],
        [0, 0, 0],
    ]
    board = board_from_rows(rows)
    assert board.clear_full_lines() == 0
    assert grid_values(board) == rows


def test_clear_full_lines_clears_rows_near_the_top_too():
    """
    The original game never cleared row 0 and left a full row 1 in
    place (a quirk of its shift-down loop). PR #5 rewrote
    clear_full_lines() and dropped that quirk on purpose, so a full row
    anywhere on the board now clears.
    """
    board = board_from_rows([
        [0, 0, 0],
        [7, 7, 7],  # full row, sitting at index 1
        [0, 0, 0],
    ])
    assert board.clear_full_lines() == 1
    assert grid_values(board) == [[0, 0, 0]] * 3


def test_clear_full_lines_clears_a_full_top_row():
    board = board_from_rows([
        [7, 7, 7],
        [0, 1, 0],
    ])
    assert board.clear_full_lines() == 1
    assert grid_values(board) == [[0, 0, 0], [0, 1, 0]]


def test_clear_full_lines_clears_two_rows_at_once():
    board = board_from_rows([[0, 0, 0], [0, 0, 0], [2, 0, 0], [7, 7, 7], [6, 6, 6]])
    assert board.clear_full_lines() == 2
    assert grid_values(board) == [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [2, 0, 0]]


def test_clear_full_lines_handles_full_rows_that_are_not_next_to_each_other():
    board = board_from_rows([
        [0, 0, 3],
        [7, 7, 7],
        [4, 0, 0],
        [6, 6, 6],
    ])
    assert board.clear_full_lines() == 2
    assert grid_values(board) == [[0, 0, 0], [0, 0, 0], [0, 0, 3], [4, 0, 0]]


def test_cells_keep_correct_positions_after_rows_shift_down():
    board = board_from_rows([
        [0, 5, 0],
        [7, 7, 7],
    ])
    board.clear_full_lines()
    for row_index, row in enumerate(board.grid):
        for col_index, cell in enumerate(row):
            assert (cell.row, cell.column) == (row_index, col_index)
