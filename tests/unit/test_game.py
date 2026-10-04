"""
Unit tests for game.py.

Game pulls in randomness (which piece type spawns next) via
random.randint(), so tests that need a predictable next piece pin it
with monkeypatch rather than looping until they get lucky. No pygame
dependency anywhere here - Game, Board, and Piece are pure logic.
"""

import random

import pytest

from game import Game
from piece import PIECE_SHAPES
from mission_data import MISSION_FIELD


def fixed_random(value):
    """Returns a stand-in for random.randint that always returns `value`."""
    return lambda a, b: value


# ---------------------------------------------------------------------
# startup / mode selection
# ---------------------------------------------------------------------

def test_game_boots_into_gameover_with_no_board_or_piece():
    """
    Matches the original's real behavior: on launch, State started as
    "gameover" and no board/piece existed yet, because initialize()
    was never called before the main loop began. This is what shows
    the "press S / M" mode-select screen on startup.
    """
    game = Game(20, 10)
    assert game.state == "gameover"
    assert game.board is None
    assert game.current_piece is None
    assert game.score == 0
    assert game.high_score == 0


def test_reset_starts_endless_mode_with_an_empty_board(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(0))
    game = Game(20, 10)
    game.reset(20, 10, is_mission=False)
    assert game.state == "start"
    assert game.board is not None
    assert all(cell == 0 for row in game.board.grid for cell in row)
    assert game.current_piece is not None


def test_reset_mission_mode_loads_the_mission_field(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(0))
    game = Game(20, 10)
    game.reset(20, 10, is_mission=True)
    assert game.state == "start"
    assert game.board.grid == MISSION_FIELD
    # confirm it's a copy, not the same list, like test_board.py checks for Board directly
    assert game.board.grid is not MISSION_FIELD


def test_reset_resets_score_but_keeps_high_score(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(0))
    game = Game(20, 10)
    game.reset(20, 10, is_mission=False)
    game.score = 10
    game.high_score = 10
    game.reset(20, 10, is_mission=False)
    assert game.score == 0
    assert game.high_score == 10  # NOT reset - matches original's HighScore persistence


# ---------------------------------------------------------------------
# spawn_piece()
# ---------------------------------------------------------------------

def test_spawn_piece_always_starts_at_x3_y0(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(2))
    game = Game(20, 10)
    game.reset(20, 10, is_mission=False)
    assert game.current_piece.type == 2
    assert game.current_piece.x == 3
    assert game.current_piece.y == 0
    assert game.current_piece.rotation == 0


# ---------------------------------------------------------------------
# movement / rotation (delegates to Board.intersects, but confirms the
# "try then revert if blocked" behavior at the Game level)
# ---------------------------------------------------------------------

def test_move_left_and_right_when_space_is_clear(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(6))  # O-piece, simplest shape
    game = Game(20, 10)
    game.reset(20, 10, is_mission=False)
    start_x = game.current_piece.x
    game.move_right()
    assert game.current_piece.x == start_x + 1
    game.move_left()
    assert game.current_piece.x == start_x


def test_move_reverts_when_blocked_by_wall(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(6))  # Figures[6][0] == [1,2,5,6]
    game = Game(3, 4)
    game.reset(3, 4, is_mission=False)
    game.current_piece.x = 2  # columns 1,2 of the shape -> already at col 3, the max legal spot
    game.move_right()  # would push column 2+1=3 -> col 4 of a width-4 board (0..3) -> illegal
    assert game.current_piece.x == 2  # move was rejected


def test_rotate_current_piece_advances_rotation(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(3))  # type 3 has 4 rotation states
    game = Game(20, 10)
    game.reset(20, 10, is_mission=False)
    game.rotate_current_piece()
    assert game.current_piece.rotation == 1


def test_rotate_reverts_when_it_would_intersect(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(3))
    game = Game(20, 10)
    game.reset(20, 10, is_mission=False)
    game.current_piece.x = -3  # jam it against the left wall
    game.rotate_current_piece()
    assert game.current_piece.rotation == 0  # rotation rejected


# ---------------------------------------------------------------------
# soft_drop() / hard_drop() / locking
# ---------------------------------------------------------------------

def test_soft_drop_moves_piece_down_by_one_when_space_is_clear(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(6))
    game = Game(20, 10)
    game.reset(20, 10, is_mission=False)
    game.soft_drop()
    assert game.current_piece.y == 1


def test_soft_drop_locks_the_piece_when_it_reaches_the_floor(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(6))  # O-piece, 2 rows tall
    game = Game(2, 10)  # a 2-row board - the piece is already at the floor
    game.reset(2, 10, is_mission=False)
    game.soft_drop()
    # the piece should have locked into the board rather than falling further
    assert game.board.grid[1][4] == game.board.grid[1][5] != 0


def test_hard_drop_drops_straight_to_the_floor_and_locks(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(6))
    game = Game(5, 10)
    game.reset(5, 10, is_mission=False)
    game.hard_drop()
    # the O-piece's bottom row should have landed on the board's last row
    assert game.board.grid[4][4] == game.board.grid[4][5] != 0


def test_locking_a_piece_scores_points_for_cleared_lines(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(6))
    game = Game(3, 4)
    game.reset(3, 4, is_mission=False)
    # pre-fill the board so the O-piece's drop completes a full row
    game.board.grid = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [9, 9, 0, 0],  # missing the two columns the piece will fill
    ]
    game.current_piece.x = 1
    game.current_piece.y = 1
    game.hard_drop()
    assert game.score == 1  # one line cleared -> 1**2 point


def test_locking_updates_high_score_only_when_beaten(monkeypatch):
    monkeypatch.setattr(random, "randint", fixed_random(6))
    game = Game(3, 4)
    game.reset(3, 4, is_mission=False)
    game.high_score = 5
    game.board.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [9, 9, 0, 0]]
    game.current_piece.x = 1
    game.current_piece.y = 1
    game.hard_drop()
    assert game.score == 1
    assert game.high_score == 5  # unchanged, since 1 < 5


def test_locking_triggers_gameover_when_the_next_piece_has_no_room(monkeypatch):
    """
    Uses a board that's only 2 rows tall (but normal width, so the
    piece legitimately spawns in-bounds). The first O-piece fills the
    entire board; the second spawn - same shape, same spawn position -
    then has nowhere to go, which should flip state to "gameover".
    """
    monkeypatch.setattr(random, "randint", fixed_random(6))  # every spawn is type 6
    game = Game(2, 10)
    game.reset(2, 10, is_mission=False)
    game.hard_drop()  # first piece fills rows 0-1 at columns 4-5
    assert game.state == "gameover"


# ---------------------------------------------------------------------
# guard asserts: methods must not be called before the game has started
# ---------------------------------------------------------------------

@pytest.mark.parametrize("method_name", [
    "move_left", "move_right", "rotate_current_piece", "soft_drop", "hard_drop",
])
def test_gameplay_methods_assert_if_called_before_reset(method_name):
    game = Game(20, 10)  # boots into "gameover", no board/piece yet
    method = getattr(game, method_name)
    with pytest.raises(AssertionError):
        method()
