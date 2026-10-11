"""
Unit tests for piece.py. No pygame dependency, no fixtures needed -
each Piece is self-contained, unlike the old global-variable version.
"""

from Elements.GameLogic.piece import Piece, PIECE_SHAPES, PIECE_COLORS


def test_piece_starts_at_given_position_with_rotation_zero():
    piece = Piece(piece_type=3, x=4, y=1)
    assert piece.x == 4
    assert piece.y == 1
    assert piece.rotation == 0


def test_piece_color_matches_its_type():
    for piece_type, expected_color in PIECE_COLORS.items():
        piece = Piece(piece_type=piece_type, x=0, y=0)
        assert piece.color == expected_color


def test_piece_image_returns_current_rotations_shape():
    piece = Piece(piece_type=0, x=0, y=0)
    assert piece.image() == PIECE_SHAPES[0][0]
    piece.rotation = 1
    assert piece.image() == PIECE_SHAPES[0][1]


def test_piece_move_updates_position_by_the_given_delta():
    piece = Piece(piece_type=0, x=3, y=0)
    piece.move(1, 2)
    assert piece.x == 4
    assert piece.y == 2
    piece.move(-2, -1)
    assert piece.x == 2
    assert piece.y == 1


def test_piece_rotate_advances_to_the_next_rotation_state():
    piece = Piece(piece_type=3, x=0, y=0)  # type 3 has 4 rotation states
    piece.rotate()
    assert piece.rotation == 1
    piece.rotate()
    assert piece.rotation == 2


def test_piece_rotate_wraps_around_after_the_last_state():
    piece = Piece(piece_type=3, x=0, y=0)
    piece.rotation = len(PIECE_SHAPES[3]) - 1  # last valid rotation
    piece.rotate()
    assert piece.rotation == 0


def test_piece_with_a_single_rotation_state_wraps_to_itself():
    piece = Piece(piece_type=6, x=0, y=0)  # type 6 only has one rotation state
    assert len(PIECE_SHAPES[6]) == 1
    piece.rotate()
    assert piece.rotation == 0
