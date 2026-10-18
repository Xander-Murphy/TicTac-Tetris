"""
Piece owns everything about a single falling tetromino: which shape it
is, where it is, which rotation it's in, and what color it should be
drawn as. Like Board, it has no pygame dependency - Game and UIMenu
each talk to it through this same small interface.

PIECE_SHAPES holds each tetromino's rotation states as flattened 4x4
grid indices (0-15), exactly as the original code did - only the name
and location changed (it used to be the global `Figures` list).
"""

PIECE_SHAPES = {
    0: [[1, 5, 9, 13], [4, 5, 6, 7]],
    1: [[4, 5, 9, 10], [2, 6, 5, 9]],
    2: [[6, 7, 9, 10], [1, 5, 6, 10]],
    3: [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    4: [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    5: [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    6: [[1, 2, 5, 6]],
}

# Index into the Colors palette (see ui.py) for each piece type -
# ported directly from the old make_figure() if/elif chain.
PIECE_COLORS = {
    0: 7,  # cyan
    1: 4,  # red
    2: 3,  # green
    3: 5,
    4: 6,
    5: 2,  # purple
    6: 1,  # yellow
}


class Piece:
    def __init__(self, piece_type, x, y):
        self.type = piece_type
        self.x = x
        self.y = y
        self.rotation = 0

    @property
    def color(self):
        return PIECE_COLORS[self.type]

    def image(self):
        """The flattened 4x4 shape for this piece's current rotation."""
        return PIECE_SHAPES[self.type][self.rotation]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        rotation_states = PIECE_SHAPES[self.type]
        self.rotation = (self.rotation + 1) % len(rotation_states)
