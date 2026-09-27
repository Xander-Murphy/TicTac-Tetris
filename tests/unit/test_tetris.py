"""
Unit tests for src/tetris.py

WHY THESE TESTS LOOK THE WAY THEY DO
-------------------------------------
tetris.py stores almost all of its game state (Height, Width, Field,
ShiftX, ShiftY, Type, Rotation, Color, Score, HighScore) as *module-level
global variables* instead of, say, fields on a Game class. That's flagged
in the code's own comments as a "code smell", and it has a direct
consequence for testing: every test has to carefully set up those
globals before calling a function, and clean them up afterwards, or
tests will bleed state into each other and fail unpredictably depending
on what order they run in.

The `reset_state` fixture below (marked `autouse=True`, meaning pytest
runs it automatically before every single test) exists specifically to
undo that problem: it resets every relevant global to a known value
before each test runs, so each test starts from a clean slate.

We also intentionally do NOT test draw_board(), draw_figure(), or
main() here. Those functions talk to pygame's screen/display/event
system, which needs a real (or virtual) display and a running event
loop. Testing them is possible but belongs in a slower "integration"
or "acceptance" test, not a fast unit test - hence your tests/unit,
tests/integration, tests/acceptance split in the project already.
"""

import random
import sys
import os

import pytest

# Make src/ importable regardless of where pytest is invoked from.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

import tetris  # noqa: E402


@pytest.fixture(autouse=True)
def reset_state():
    """
    Runs before EVERY test automatically (autouse=True).

    Resets tetris's global variables to known, predictable values so
    that no test can accidentally see leftover state from a previous
    test (e.g. a Score that was incremented by a different test).
    """
    tetris.Height = 20
    tetris.Width = 10
    tetris.Field = [[0] * tetris.Width for _ in range(tetris.Height)]
    tetris.Type = 0
    tetris.Color = 0
    tetris.Rotation = 0
    tetris.ShiftX = 0
    tetris.ShiftY = 0
    tetris.Score = 0
    tetris.HighScore = 0
    tetris.State = "start"
    yield
    # (nothing needed after the test; the next test's setup will
    # overwrite everything again anyway)


# ---------------------------------------------------------------------
# make_figure()
# ---------------------------------------------------------------------

def test_make_figure_sets_shift_position():
    tetris.make_figure(3, 0)
    assert tetris.ShiftX == 3
    assert tetris.ShiftY == 0


def test_make_figure_resets_rotation_to_zero():
    tetris.Rotation = 2  # pretend a previous figure had been rotated
    tetris.make_figure(3, 0)
    assert tetris.Rotation == 0


def test_make_figure_assigns_color_matching_type(monkeypatch):
    """
    make_figure() picks a random Type, then maps that Type to a fixed
    Color via an if/elif chain. Rather than test "the color is random"
    (which would be flaky), we pin the randomness with monkeypatch so
    we can assert the exact mapping the code promises.
    """
    expected_color_by_type = {
        0: 7,  # cyan
        1: 4,  # red
        2: 3,  # green
        3: 5,
        4: 6,
        5: 2,  # purple
        6: 1,  # yellow
    }
    for fig_type, expected_color in expected_color_by_type.items():
        monkeypatch.setattr(random, "randint", lambda a, b, t=fig_type: t)
        tetris.make_figure(3, 0)
        assert tetris.Type == fig_type
        assert tetris.Color == expected_color


# ---------------------------------------------------------------------
# init_board() / initialize()
# ---------------------------------------------------------------------

def test_init_board_creates_correct_dimensions():
    tetris.Height = 5
    tetris.Width = 4
    tetris.Field = []
    tetris.init_board()
    assert len(tetris.Field) == 5
    assert all(len(row) == 4 for row in tetris.Field)
    assert all(cell == 0 for row in tetris.Field for cell in row)


def test_initialize_endless_mode_starts_with_empty_field():
    tetris.initialize(20, 10, False)
    assert tetris.State == "start"
    assert tetris.Height == 20
    assert tetris.Width == 10
    assert all(cell == 0 for row in tetris.Field for cell in row)


def test_initialize_mission_mode_uses_mission_field():
    tetris.initialize(20, 10, True)
    assert tetris.Field is tetris.MissionField
    # spot check a couple of known non-zero cells from MissionField
    assert tetris.Field[12][1] == 5
    assert tetris.Field[13][0] == 1


# ---------------------------------------------------------------------
# intersects()
# ---------------------------------------------------------------------
# intersects() checks a 4x4 "image" (a list of cell indices 0-15, read
# as a 4x4 grid: index = row*4 + col) against the board edges and
# against cells that are already filled in Field.

SQUARE_IMAGE = [1, 2, 5, 6]  # a 2x2 block: row0 cols1-2, row1 cols1-2


def test_intersects_false_when_space_is_clear():
    tetris.ShiftX = 0
    tetris.ShiftY = 0
    assert tetris.intersects(SQUARE_IMAGE) is False


def test_intersects_true_when_past_right_wall():
    tetris.Width = 3          # board is only 3 columns wide (indices 0,1,2)
    tetris.ShiftX = 2         # SQUARE_IMAGE needs columns 1 and 2 -> col 2+2=4, out of range
    tetris.ShiftY = 0
    assert tetris.intersects(SQUARE_IMAGE) is True


def test_intersects_true_when_past_left_wall():
    tetris.ShiftX = -2        # pushes the block's column 1 to -1, off the left edge
    tetris.ShiftY = 0
    assert tetris.intersects(SQUARE_IMAGE) is True


def test_intersects_true_when_past_bottom():
    tetris.Height = 2         # board is only 2 rows tall
    tetris.ShiftX = 0
    tetris.ShiftY = 1         # SQUARE_IMAGE needs row 1 -> row 1+1=2, out of range
    assert tetris.intersects(SQUARE_IMAGE) is True


def test_intersects_true_when_overlapping_filled_cell():
    tetris.ShiftX = 0
    tetris.ShiftY = 0
    tetris.Field[1][2] = 4  # occupy a cell the SQUARE_IMAGE would land on
    assert tetris.intersects(SQUARE_IMAGE) is True


# ---------------------------------------------------------------------
# go_side() / rotate()
# ---------------------------------------------------------------------

def test_go_side_moves_left_and_right_when_clear():
    tetris.Type = 6
    tetris.Rotation = 0
    tetris.ShiftX = 3
    tetris.ShiftY = 0
    tetris.go_side(1)
    assert tetris.ShiftX == 4
    tetris.go_side(-1)
    assert tetris.ShiftX == 3


def test_go_side_reverts_move_when_it_would_hit_wall():
    tetris.Width = 10
    tetris.Type = 6           # Figures[6][0] == [1, 2, 5, 6]
    tetris.Rotation = 0
    tetris.ShiftX = 8         # column 2 + 8 = 10, already the max legal position
    tetris.ShiftY = 0
    tetris.go_side(1)         # would push it to column 11 -> illegal
    assert tetris.ShiftX == 8  # move was rejected, position unchanged


def test_rotate_advances_to_next_rotation_state():
    tetris.Type = 3  # this figure has 4 rotation states
    tetris.Rotation = 0
    tetris.ShiftX = 3
    tetris.ShiftY = 3
    tetris.rotate()
    assert tetris.Rotation == 1


def test_rotate_wraps_around_after_last_rotation_state():
    tetris.Type = 3  # 4 rotation states: 0,1,2,3
    tetris.Rotation = 3
    tetris.ShiftX = 3
    tetris.ShiftY = 3
    tetris.rotate()
    assert tetris.Rotation == 0


def test_rotate_reverts_when_new_rotation_would_intersect():
    tetris.Type = 3
    tetris.Rotation = 0
    tetris.ShiftX = 0
    tetris.ShiftY = 0
    # push the piece hard against the left wall so rotating into a
    # wider shape is guaranteed to go out of bounds
    tetris.ShiftX = -3
    tetris.rotate()
    assert tetris.Rotation == 0  # rotation was rejected


# ---------------------------------------------------------------------
# break_lines()
# ---------------------------------------------------------------------

def test_break_lines_clears_a_full_row_and_scores_a_point():
    """
    NOTE ON A QUIRK THIS TEST UNCOVERED:
    break_lines() only checks rows starting at index 1 (never row 0),
    and when it clears a full row at index `i` it copies row `i-1`
    down into it via `for k in range(i, 1, -1)`. If the full row is
    AT index 1, that range is empty, so nothing gets copied down and
    the "cleared" row is left unchanged. That means a full row at the
    very top of the checked area doesn't visually clear, even though
    it still scores a point. This test avoids that index-1 special
    case (by putting the full row at index 2) so it exercises the
    normal shift-down path; the special case is worth asking the
    original author about, since it looks unintentional.
    """
    tetris.Height = 4
    tetris.Width = 3
    tetris.Field = [
        [0, 0, 0],
        [1, 0, 0],
        [9, 9, 9],  # full row -> should be cleared
        [0, 0, 0],
    ]
    tetris.Score = 0
    tetris.break_lines()
    assert tetris.Score == 1  # one line cleared -> 1**2 == 1 point
    # row 1's contents should have shifted down into row 2
    assert tetris.Field[2] == [1, 0, 0]


def test_break_lines_does_nothing_when_no_row_is_full():
    tetris.Height = 4
    tetris.Width = 3
    original_field = [
        [0, 0, 0],
        [9, 9, 0],  # not full - one empty cell
        [1, 0, 0],
        [0, 0, 0],
    ]
    tetris.Field = [row[:] for row in original_field]
    tetris.Score = 0
    tetris.break_lines()
    assert tetris.Score == 0
    assert tetris.Field == original_field


def test_break_lines_updates_high_score_only_when_beaten():
    tetris.Height = 3
    tetris.Width = 2
    tetris.Field = [[0, 0], [9, 9], [0, 0]]
    tetris.Score = 0
    tetris.HighScore = 5
    tetris.break_lines()          # scores 1 point -> Score becomes 1
    assert tetris.Score == 1
    assert tetris.HighScore == 5  # unchanged, since 1 < 5

    tetris.Field = [[0, 0], [9, 9], [0, 0]]
    tetris.break_lines()          # scores another point -> Score becomes 2
    assert tetris.HighScore == 5  # still unchanged, since 2 < 5


# ---------------------------------------------------------------------
# freeze() / go_down() / go_space()
# ---------------------------------------------------------------------

def test_freeze_writes_the_figures_color_into_the_field(monkeypatch):
    monkeypatch.setattr(random, "randint", lambda a, b: 0)  # next spawn is deterministic
    tetris.Type = 6           # Figures[6][0] == [1, 2, 5, 6]
    tetris.Rotation = 0
    tetris.Color = 4
    tetris.ShiftX = 0
    tetris.ShiftY = 0
    tetris.freeze(tetris.Figures[tetris.Type][tetris.Rotation])
    assert tetris.Field[0][1] == 4
    assert tetris.Field[0][2] == 4
    assert tetris.Field[1][1] == 4
    assert tetris.Field[1][2] == 4


def test_freeze_spawns_a_new_figure_after_locking(monkeypatch):
    monkeypatch.setattr(random, "randint", lambda a, b: 0)  # next figure will be Type 0
    tetris.Type = 6
    tetris.Rotation = 0
    tetris.Color = 4
    tetris.ShiftX = 0
    tetris.ShiftY = 0
    tetris.freeze(tetris.Figures[tetris.Type][tetris.Rotation])
    assert tetris.Type == 0       # make_figure() was called and picked Type 0
    assert tetris.ShiftX == 3     # make_figure(3, 0) is always called after freezing
    assert tetris.ShiftY == 0


def test_freeze_sets_gameover_when_new_figure_has_no_room(monkeypatch):
    """
    If the stack is already too tall for the newly spawned figure to
    fit, freeze() should flip State to "gameover".
    """
    monkeypatch.setattr(random, "randint", lambda a, b: 6)  # next spawn: Type 6
    tetris.Width = 4  # deliberately narrow, so Type 6 spawned at x=3 won't fit
    tetris.Field = [[0] * tetris.Width for _ in range(tetris.Height)]
    tetris.Type = 6
    tetris.Rotation = 0
    tetris.Color = 4
    tetris.ShiftX = 0
    tetris.ShiftY = 0
    tetris.State = "start"
    tetris.freeze(tetris.Figures[tetris.Type][tetris.Rotation])
    assert tetris.State == "gameover"


def test_go_down_moves_the_piece_down_by_one_when_space_is_clear():
    tetris.Type = 6
    tetris.Rotation = 0
    tetris.ShiftX = 3
    tetris.ShiftY = 0
    tetris.go_down()
    assert tetris.ShiftY == 1


def test_go_down_locks_the_piece_when_it_reaches_the_floor(monkeypatch):
    monkeypatch.setattr(random, "randint", lambda a, b: 0)
    tetris.Height = 2  # very short board so the piece hits bottom immediately
    tetris.Field = [[0] * tetris.Width for _ in range(tetris.Height)]
    tetris.Type = 6
    tetris.Rotation = 0
    tetris.Color = 4
    tetris.ShiftX = 3
    tetris.ShiftY = 0
    tetris.go_down()
    # the piece should have been frozen into the field rather than
    # moving past the floor
    assert tetris.Field[1][4] == 4
    assert tetris.Field[1][5] == 4


def test_go_space_drops_the_piece_all_the_way_to_the_floor(monkeypatch):
    monkeypatch.setattr(random, "randint", lambda a, b: 0)
    tetris.Height = 5
    tetris.Field = [[0] * tetris.Width for _ in range(tetris.Height)]
    tetris.Type = 6  # Figures[6][0] == [1, 2, 5, 6]
    tetris.Rotation = 0
    tetris.Color = 4
    tetris.ShiftX = 3
    tetris.ShiftY = 0
    tetris.go_space()
    # the 2x2 block's bottom row should have landed on the last row (index 4)
    assert tetris.Field[4][4] == 4
    assert tetris.Field[4][5] == 4