from enum import Enum


class CellStatus(Enum):
    EMPTY = 0
    FILLED = 1
    PREVIEW = 2


class Cell:
    def __init__(self, row, column, status=CellStatus.EMPTY, tileTexture=0):
        self.row = row
        self.column = column
        self.status = status
        self.tileTexture = tileTexture

    def clear(self):
        self.status = CellStatus.EMPTY
        self.tileTexture = 0          # Set to empty texture