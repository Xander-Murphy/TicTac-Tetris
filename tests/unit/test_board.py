"""
Unit tests for board.py.

Board has no pygame dependency, so these tests need no display and run
fast. Where a test needs a "piece", we use the real Piece class rather
than a hand-rolled fake - Board.intersects()/lock_piece() only need an
object with .x, .y, .image() and .color, which Piece already is.
"""

from Elements.GameLogic.board import Board
from Elements.GameLogic.piece import Piece


# A simple 2x2 square piece (Type 6, rotation 0) is used throughout as
# a predictable shape: image() == [1, 2, 5, 6], i.e. a 2-row, 2-col
# block occupying (row+0,col+1), (row+0,col+2), (row+1,col+1), (row+1,col+2).
def square_piece(x, y):
    return Piece(piece_type=6, x=x, y=y)


# ---------------------------------------------------------------------
# construction
# ---------------------------------------------------------------------

def test_empty_board_has_correct_dimensions_and_all_zero_cells():
    board = Board(height=5, width=4)
    assert board.height == 5
    assert board.width == 4
    assert len(board.grid) == 5
    assert all(len(row) == 4 for row in board.grid)
    assert all(cell == 0 for row in board.grid for cell in row)


def test_board_with_initial_grid_copies_rather_than_aliases():
    """
    Mission mode passes in a shared MISSION_FIELD constant. If Board
    stored that list by reference instead of copying it, playing one
    mission-mode game would permanently mutate MISSION_FIELD for every
    future game. This guards against that.
    """
    original = [[0, 0], [0, 0]]
    board = Board(height=2, width=2, initial_grid=original)
    board.grid[0][0] = 9
    assert original[0][0] == 0  # original untouched


def test_is_cell_occupied():
    board = Board(height=2, width=2)
    assert board.is_cell_occupied(0, 0) is False
    board.grid[0][0] = 3
    assert board.is_cell_occupied(0, 0) is True


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
    board.grid[1][2] = 4  # occupy a cell the square piece would land on
    piece = square_piece(x=0, y=0)
    assert board.intersects(piece) is True


# ---------------------------------------------------------------------
# lock_piece()
# ---------------------------------------------------------------------

def test_lock_piece_writes_the_pieces_color_into_the_grid():
    board = Board(height=5, width=5)
    piece = square_piece(x=0, y=0)
    board.lock_piece(piece)
    expected_color = piece.color
    assert board.grid[0][1] == expected_color
    assert board.grid[0][2] == expected_color
    assert board.grid[1][1] == expected_color
    assert board.grid[1][2] == expected_color
    # cells outside the shape stay empty
    assert board.grid[0][0] == 0


# ---------------------------------------------------------------------
# clear_full_lines()
# ---------------------------------------------------------------------

def test_clear_full_lines_clears_a_full_row_and_returns_count():
    board = Board(height=4, width=3)
    board.grid = [
        [0, 0, 0],
        [1, 0, 0],
        [9, 9, 9],  # full row
        [0, 0, 0],
    ]
    lines_cleared = board.clear_full_lines()
    assert lines_cleared == 1
    # row 1's contents should have shifted down into row 2
    assert board.grid[2] == [1, 0, 0]


def test_clear_full_lines_does_nothing_when_no_row_is_full():
    board = Board(height=4, width=3)
    original = [
        [0, 0, 0],
        [9, 9, 0],  # one empty cell - not full
        [1, 0, 0],
        [0, 0, 0],
    ]
    board.grid = [row[:] for row in original]
    lines_cleared = board.clear_full_lines()
    assert lines_cleared == 0
    assert board.grid == original


def test_clear_full_lines_row_index_1_quirk_is_preserved():
    """
    This documents a quirk ported from the original game: row index 1
    is never actually overwritten by the shift-down logic (there's
    nothing "above" it to copy from, since row 0 is never touched).
    So a full row sitting exactly at index 1 still counts toward the
    score, but visually stays in place instead of clearing. This test
    exists so that if someone "fixes" this later, it's a deliberate,
    visible decision rather than an accidental side effect.
    """
    board = Board(height=3, width=3)
    board.grid = [
        [0, 0, 0],
        [9, 9, 9],  # full row, sitting at index 1
        [0, 0, 0],
    ]
    lines_cleared = board.clear_full_lines()
    assert lines_cleared == 1
    assert board.grid[1] == [9, 9, 9]  # unchanged, per the quirk above
