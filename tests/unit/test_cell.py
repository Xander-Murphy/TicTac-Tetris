"""Unit tests for cell.py - one square of the board."""

from elements.gameLogic.cell import Cell, CellStatus


def test_new_cell_is_empty_with_the_empty_texture():
    cell = Cell(3, 4)
    assert (cell.row, cell.column) == (3, 4)
    assert cell.status is CellStatus.EMPTY
    assert cell.tileTexture == 0


def test_cell_can_start_filled_with_a_texture():
    cell = Cell(0, 0, CellStatus.FILLED, 5)
    assert cell.status is CellStatus.FILLED
    assert cell.tileTexture == 5


def test_clear_empties_the_cell_and_resets_its_texture():
    cell = Cell(1, 1, CellStatus.FILLED, 6)
    cell.clear()
    assert cell.status is CellStatus.EMPTY
    assert cell.tileTexture == 0
    assert (cell.row, cell.column) == (1, 1)  # position is untouched
