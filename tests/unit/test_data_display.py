import pygame

from elements.UI.dataDisplay import DataDisplay
from elements.UI.gameUI import GameUI
from elements.config import Config
from elements.gameLogic.board import Board


def test_data_display_composes_child_surfaces_and_draws_at_position(screen):
    display = DataDisplay((20, 15), (30, 40))
    child = pygame.Surface((4, 3))
    child.fill((255, 0, 0))

    display.add_surface(child, (5, 6))
    display.display(screen)

    assert display.surface.get_size() == (20, 15)
    assert display.size == (20, 15)
    assert display.position == (30, 40)
    assert display.surface.get_at((5, 6)) == pygame.Color(255, 0, 0, 255)
    assert screen.get_at((35, 46)) == pygame.Color(255, 0, 0, 255)
    assert screen.get_at((30, 40)) == pygame.Color(0, 0, 255, 255)
    assert screen.get_at((49, 54)) == pygame.Color(0, 0, 255, 255)

    display.clear()
    display.display(screen)

    assert screen.get_at((35, 46)) == pygame.Color(255, 255, 255, 255)
    assert screen.get_at((30, 40)) == pygame.Color(0, 0, 255, 255)


def test_game_ui_initializes_score_and_next_piece_displays(screen):
    ui = GameUI(screen)
    board = Board(20, 10)

    ui.initialize_board(board)
    ui.draw_hud(12, 34)

    board_position = (
        (Config.SCREEN_SIZE[0] - board.width * ui.cell_size) // 2,
        (Config.SCREEN_SIZE[1] - board.height * ui.cell_size) // 2,
    )
    next_piece_size = board.height * ui.cell_size // 3

    assert ui.score_data_display.position == (0, 0)
    assert ui.score_data_display.surface.get_bounding_rect().width > 0
    assert ui.next_piece_data_display.size == (next_piece_size, next_piece_size)
    assert ui.next_piece_data_display.position == (
        board_position[0] + board.width * ui.cell_size + ui.cell_size,
        board_position[1],
    )
    assert ui.next_piece_data_display.surface.get_bounding_rect().size == (0, 0)
    assert screen.get_at(ui.next_piece_data_display.position) == pygame.Color(0, 0, 255, 255)
