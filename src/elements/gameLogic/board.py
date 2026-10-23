"""
Board owns the game grid and everything that operates purely on grid
state: collision checks, locking a piece into place, and clearing full
rows. It has zero knowledge of pygame, input, or rendering - that
separation is what lets Board (and Game, and Piece) be unit tested
without ever opening a window.
"""

from .cell import Cell, CellStatus


class Board:
    def __init__(self, height, width, initial_grid=None):
        """
        initial_grid: optional starting layout (used by mission mode).
        Pass None for a normal empty board.
        """
        self.height = height
        self.width = width
        
        self.grid = [
            [Cell(row, col) for col in range(width)] for row in range(height)
        ]
        
        if initial_grid is not None:
            # Create normal grid
            # Set status and texture index of cells with values above 0
            self.grid = [
                [
                    Cell(row_index, col_index, CellStatus.FILLED, value) if value > 0 else Cell(row_index, col_index) 
                    for col_index, value in enumerate(row)
                ] for row_index, row in enumerate(initial_grid)
            ]

    def is_cell_occupied(self, cell : Cell):
        return cell.status is CellStatus.FILLED

    def get_cell(self, row, col):
            cell : Cell = self.grid[row][col]
            return cell

    def intersects(self, piece):
        """
        True if `piece`, at its current position/rotation, would go out
        of bounds or overlap an already-filled cell.
        """
        pieceDimentions : int = 4   # Pieces have a fixed 1:1 aspect ratio

        for pieceImageY in range(pieceDimentions):
            for pieceImangeX in range(pieceDimentions):
                if pieceImageY * pieceDimentions + pieceImangeX in piece.image(): 
                # Finds what part of the piece image is actually
                # Column values are a rows length away from the next column value
                # For example notice the first column
                # 0   1   2   3
                # 4   5   6   7
                # 8   9   10  11
                # 12  13  14  15
                    row = piece.y + pieceImageY   
                    col = piece.x + pieceImangeX
                    # Piece origin x y is 0,0
                    if (
                        row > self.height - 1                          # Below the board
                        or col > self.width - 1  or col < 0            # Left or right out of the board
                        or self.is_cell_occupied(self.grid[row][col])  # If cell is already filled
                    ):
                        return True
        return False

    def lock_piece(self, piece):
        """Burn a piece's current shape/color permanently into the grid."""
        pieceDimentions : int = 4   # Pieces have a fixed 1:1 aspect ratio
       
        for pieceImageY in range(pieceDimentions):
            for pieceImangeX in range(pieceDimentions):
                if pieceImageY * pieceDimentions + pieceImangeX in piece.image(): 

                    row = piece.y + pieceImageY   
                    col = piece.x + pieceImangeX
                    
                    cell : Cell = self.grid[row][col]
                    cell.status = CellStatus.FILLED
                    cell.tileTexture = piece.color

    def clear_full_lines(self):
        """
        Removes every full row, shifts remaining rows down, and adds
        empty rows at the top. Returns the number of lines cleared.
        """
        lines_cleared = 0

        for row_index in range(self.height - 1, -1, -1): # Bottom to top
            row = self.grid[row_index]
            if all(self.is_cell_occupied(cell) for cell in row):
                lines_cleared += 1
                continue

            destination = row_index + lines_cleared
            if destination != row_index:
                self.grid[destination] = row
                for column, cell in enumerate(row):
                    cell.row = destination
                    cell.column = column

        for row_index in range(lines_cleared):
            self.grid[row_index] = [
                Cell(row_index, column) for column in range(self.width)
            ]

        return lines_cleared
