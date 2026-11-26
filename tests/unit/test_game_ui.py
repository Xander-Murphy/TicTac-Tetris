"""GameUI input handling and drawing, using a RecordingGame in place of a real Game."""

import pygame
import pytest

from elements.UI.gameUI import GameUI, RED
from elements.UI.textures import Texture
from elements.gameLogic.board import Board
from elements.gameLogic.piece import Piece
from elements.missionData.mission_data import MISSION_BOARDS


class RecordingGame:
    def __init__(self, state, is_mission=False):
        self.state = state
        self.is_mission = is_mission
        self.calls = []

    def __getattr__(self, name):
        return lambda *args, **kwargs: self.calls.append((name, *args, *kwargs.values()))


# ---------------------------------------------------------------------
# keys while playing
# ---------------------------------------------------------------------

@pytest.mark.parametrize("key, expected", [
    (pygame.K_UP, ("rotate_current_piece",)),
    (pygame.K_LEFT, ("move_left",)),
    (pygame.K_RIGHT, ("move_right",)),
    (pygame.K_SPACE, ("hard_drop",)),
])
def test_playing_keys_call_the_matching_game_method(screen, send_keys, key, expected):
    game = RecordingGame("start")
    send_keys(key)
    GameUI(screen).handle_input(game)
    assert game.calls == [expected]


@pytest.mark.parametrize("key", [pygame.K_r, pygame.K_m, pygame.K_q])
def test_game_over_keys_do_nothing_while_playing(screen, send_keys, quit_calls, scene_changes, key):
    game = RecordingGame("start")
    send_keys(key)
    GameUI(screen).handle_input(game)
    assert game.calls == [] and quit_calls == [] and scene_changes == []


def test_down_key_is_tracked_until_released(screen, send_keys, monkeypatch):
    ui, game = GameUI(screen), RecordingGame("start")
    send_keys(pygame.K_DOWN)
    ui.handle_input(game)
    assert ui.pressing_down is True

    release = pygame.event.Event(pygame.KEYUP, key=pygame.K_DOWN)
    monkeypatch.setattr(pygame.event, "get", lambda *a: [release])
    ui.handle_input(game)
    assert ui.pressing_down is False


def test_closing_the_window_quits(screen, monkeypatch, quit_calls):
    monkeypatch.setattr(pygame.event, "get", lambda *a: [pygame.event.Event(pygame.QUIT)])
    GameUI(screen).handle_input(RecordingGame("start"))
    assert quit_calls == ["quit"]


# ---------------------------------------------------------------------
# keys on the game-over screen
# ---------------------------------------------------------------------

@pytest.mark.parametrize("is_mission", [False, True])
def test_r_restarts_in_the_same_mode(screen, send_keys, is_mission):
    game = RecordingGame("gameover", is_mission=is_mission)
    send_keys(pygame.K_r)
    GameUI(screen).handle_input(game)
    assert game.calls == [("reset", 20, 10, is_mission, 0)]


def test_r_clears_a_held_down_key(screen, send_keys):
    ui = GameUI(screen)
    ui.pressing_down = True
    send_keys(pygame.K_r)
    ui.handle_input(RecordingGame("gameover"))
    assert ui.pressing_down is False


def test_m_goes_back_to_the_main_menu_from_the_current_scene(screen, send_keys, scene_changes):
    send_keys(pygame.K_m)
    GameUI(screen).handle_input(RecordingGame("gameover"), "missionTestScene")
    assert scene_changes == [("missionTestScene", "startScene")]


def test_q_on_the_game_over_screen_quits(screen, send_keys, quit_calls):
    send_keys(pygame.K_q)
    GameUI(screen).handle_input(RecordingGame("gameover"))
    assert quit_calls == ["quit"]


def test_right_and_left_pick_the_mission_board_for_the_next_restart(screen, send_keys):
    ui, game = GameUI(screen), RecordingGame("gameover", is_mission=True)
    send_keys(pygame.K_RIGHT)
    ui.handle_input(game)
    assert ui.mission_selected == 1

    send_keys(pygame.K_r)
    ui.handle_input(game)
    assert game.calls == [("reset", 20, 10, True, 1)]


@pytest.mark.parametrize("key, expected", [
    (pygame.K_LEFT, len(MISSION_BOARDS) - 1),  # wraps from the first to the last
    (pygame.K_RIGHT, 1 % len(MISSION_BOARDS)),
])
def test_mission_board_choice_wraps_around(screen, send_keys, key, expected):
    ui = GameUI(screen)
    send_keys(key)
    ui.handle_input(RecordingGame("gameover", is_mission=True))
    assert ui.mission_selected == expected


def test_mission_board_choice_is_ignored_in_endless_mode(screen, send_keys):
    ui = GameUI(screen)
    send_keys(pygame.K_RIGHT)
    ui.handle_input(RecordingGame("gameover", is_mission=False))
    assert ui.mission_selected == 0


# ---------------------------------------------------------------------
# drawing
# ---------------------------------------------------------------------

def screen_point(ui, row, col):
    """Center of a board cell, in screen coordinates."""
    x, y = ui.board_position
    half = ui.cell_size // 2
    return (x + col * ui.cell_size + half, y + row * ui.cell_size + half)


def test_draw_board_paints_filled_cells_in_their_tile_color(screen):
    ui, board = GameUI(screen), Board(20, 10, [[0] * 10] * 19 + [[3] + [0] * 9])
    ui.draw_board(board)
    assert screen.get_at(screen_point(ui, 19, 0))[:3] == Texture.getTileTexture(3)
    assert screen.get_at(screen_point(ui, 19, 1))[:3] == Texture.getTileTexture(0)


def test_draw_piece_uses_the_pieces_fixed_color(screen):
    ui, board = GameUI(screen), Board(20, 10)
    piece = Piece(piece_type=6, x=3, y=0)  # O-piece covers (0,4), (0,5), (1,4), (1,5)
    ui.draw_board(board)
    ui.draw_piece(piece, board)
    assert screen.get_at(screen_point(ui, 0, 4))[:3] == Texture.getTileTexture(piece.color)


def goal_row_outline_pixel(ui, row):
    x, y = ui.board_position
    return (x + ui.cell_size * 3 + ui.cell_size // 2, y + row * ui.cell_size)


def test_goal_row_is_outlined_in_red(screen):
    ui = GameUI(screen)
    ui.draw_board(Board(20, 10), goal_row=17)
    assert screen.get_at(goal_row_outline_pixel(ui, 17))[:3] == RED


def test_no_red_outline_without_a_goal_row(screen):
    ui = GameUI(screen)
    ui.draw_board(Board(20, 10))
    assert screen.get_at(goal_row_outline_pixel(ui, 17))[:3] != RED


def test_update_ui_draws_board_piece_and_hud(screen):
    ui = GameUI(screen)
    ui.update_UI(Board(20, 10), Piece(0, 3, 0), score=3, high_score=9, goal_row=17)
    assert ui.is_board_initialized and ui.is_data_displays_initialized


def test_draw_hud_before_the_board_raises(screen):
    with pytest.raises(RuntimeError):
        GameUI(screen).draw_hud(0, 0)


def test_game_over_screen_draws_without_errors_in_both_modes(screen):
    ui = GameUI(screen)
    ui.draw_game_over_screen()
    ui.draw_game_over_screen(is_mission=True)


def test_game_over_screen_blits_its_surface_to_the_screen(screen):
    screen.fill((10, 20, 30))
    ui = GameUI(screen, RecordingGame("gameover"))

    ui.draw_game_over_screen()

    assert screen.get_at((16, 256))[:3] == (0, 0, 0)


def test_draw_hud_renders_the_next_piece_in_its_display_grid(screen):
    game = RecordingGame("start")
    game.next_piece = Piece(0, 3, 0)
    ui = GameUI(screen, game)
    ui.initialize_board(Board(20, 10))

    ui.draw_hud(score=0, high_score=0)

    display = ui.next_piece_data_display
    grid_offset = (
        (display.size[0] - display.size[0] // 2) // 2,
        (display.size[1] - display.size[1] // 2) // 2,
    )
    cell_size = (display.size[0] // 2) // 4
    first_occupied_cell = (
        display.position[0] + grid_offset[0] + cell_size + cell_size // 2,
        display.position[1] + grid_offset[1] + cell_size // 2,
    )

    assert screen.get_at(first_occupied_cell)[:3] == Texture.getTileTexture(game.next_piece.color)
