"""
Board owns the game grid and everything that operates purely on grid
state: collision checks, locking a piece into place, and clearing full
rows. It has zero knowledge of pygame, input, or rendering - that
separation is what lets Board (and Game, and Piece) be unit tested
without ever opening a window.
"""


class Board:
    def __init__(self, height, width, initial_grid=None):
        """
        initial_grid: optional starting layout (used by mission mode).
        Pass None for a normal empty board.
        """
        self.height = height
        self.width = width
        if initial_grid is not None:
            # copy rows so mutating this board never mutates the
            # caller's original data (e.g. a shared MISSION_FIELD constant)
            self.grid = [row[:] for row in initial_grid]
        else:
            self.grid = [[0] * width for _ in range(height)]

    def is_cell_occupied(self, row, col):
        return self.grid[row][col] > 0

    def intersects(self, piece):
        """
        True if `piece`, at its current position/rotation, would go out
        of bounds or overlap an already-filled cell.
        """
        for i in range(4):
            for j in range(4):
                if i * 4 + j in piece.image():
                    row = piece.y + i
                    col = piece.x + j
                    if (
                        row > self.height - 1
                        or col > self.width - 1
                        or col < 0
                        or self.grid[row][col] > 0
                    ):
                        return True
        return False

    def lock_piece(self, piece):
        """Burn a piece's current shape/color permanently into the grid."""
        for i in range(4):
            for j in range(4):
                if i * 4 + j in piece.image():
                    self.grid[piece.y + i][piece.x + j] = piece.color

    def clear_full_lines(self):
        """
        Removes every full row and shifts the rows above it down.
        Returns the number of lines cleared (Game uses this to score).

        NOTE: row 0 is intentionally never checked or targeted, matching
        the original game's behavior - it acts as an unused top buffer
        row. This was ported as-is rather than "fixed", since changing
        it changes gameplay feel; flagging it here in case that's worth
        revisiting later.
        """
        lines_cleared = 0
        for i in range(1, self.height):
            if all(cell != 0 for cell in self.grid[i]):
                lines_cleared += 1
                for k in range(i, 1, -1):
                    self.grid[k] = self.grid[k - 1][:]
        return lines_cleared
