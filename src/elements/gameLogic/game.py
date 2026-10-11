"""
Game is the coordinator described in Design.md/Architecture.md: it owns
a Board and the current Piece (composition), and exposes a small set of
verbs (move_left, move_right, soft_drop, hard_drop, rotate_current_piece)
that UIMenu/main.py call in response to input. Nothing outside Game
needs to know how movement, locking, or line-clearing actually work -
that's the abstraction boundary.

Like Board and Piece, Game has no pygame dependency, so all of this
can be unit tested with no display attached.
"""

import random

from elements.gameLogic.board import Board
from elements.gameLogic.piece import Piece, PIECE_SHAPES
from elements.missionData.mission_data import MISSION_FIELD


class Game:
    def __init__(self, height, width):
        """
        Matches the original's actual startup behavior: the global
        State started as "gameover" and initialize()/make_figure() were
        never called before the loop began (they were commented out).
        So the game boots straight to the game-over/mode-select screen,
        with no board or piece yet - not into "start".
        """
        self.height = height
        self.width = width
        self.score = 0
        self.high_score = 0
        self.state = "gameover"
        self.is_mission = False
        self.board = None
        self.current_piece = None

    def reset(self, height, width, is_mission=False):
        """
        Starts a fresh round. Deliberately keeps high_score across
        resets, matching the original game's behavior (HighScore
        persisted across restarts, only Score reset to 0).
        """
        self.height = height
        self.width = width
        self.is_mission = is_mission
        initial_grid = MISSION_FIELD if is_mission else None
        self.board = Board(height, width, initial_grid)
        self.score = 0
        self.state = "start"
        self.spawn_piece()

    def spawn_piece(self):
        piece_type = random.randint(0, len(PIECE_SHAPES) - 1)
        self.current_piece = Piece(piece_type, x=3, y=0)

    def move_left(self):
        self._try_move(-1, 0)

    def move_right(self):
        self._try_move(1, 0)

    def _try_move(self, dx, dy):
        assert self.board is not None and self.current_piece is not None, \
            "_try_move() called before the game has started"
        self.current_piece.move(dx, dy)
        if self.board.intersects(self.current_piece):
            self.current_piece.move(-dx, -dy)  # revert

    def rotate_current_piece(self):
        assert self.board is not None and self.current_piece is not None, \
            "rotate_current_piece() called before the game has started"
        old_rotation = self.current_piece.rotation
        self.current_piece.rotate()
        if self.board.intersects(self.current_piece):
            self.current_piece.rotation = old_rotation  # revert

    def soft_drop(self):
        """Move the current piece down one row, locking it if it can't."""
        assert self.board is not None and self.current_piece is not None, \
            "soft_drop() called before the game has started"
        self.current_piece.move(0, 1)
        if self.board.intersects(self.current_piece):
            self.current_piece.move(0, -1)
            self._lock_and_advance()

    def hard_drop(self):
        """Drop the current piece straight to the floor and lock it."""
        assert self.board is not None and self.current_piece is not None, \
            "hard_drop() called before the game has started"
        while not self.board.intersects(self.current_piece):
            self.current_piece.move(0, 1)
        self.current_piece.move(0, -1)
        self._lock_and_advance()

    def _lock_and_advance(self):
        assert self.board is not None and self.current_piece is not None, \
            "_lock_and_advance() called before the game has started"
        self.board.lock_piece(self.current_piece)
        lines_cleared = self.board.clear_full_lines()
        self.score += lines_cleared ** 2
        if self.high_score < self.score:
            self.high_score = self.score

        self.spawn_piece()
        if self.board.intersects(self.current_piece):
            self.state = "gameover"