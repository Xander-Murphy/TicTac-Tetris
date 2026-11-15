"""
Integration: the real SceneManager, game scenes, GameUI, Game, Board and
Piece working together. Only key presses and the screen are faked.
"""

import os
import random

import pygame
import pytest

from elements.eventManager import EventManager
from elements.missionData.mission_data import MISSION_GOAL_ROW
from elements.sceneManager import SceneManager
from grid_helpers import is_filled

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


@pytest.fixture
def open_scene(screen, monkeypatch):
    """open_scene("endlessTestScene") -> a SceneManager showing that scene."""
    monkeypatch.setattr(random, "randint", lambda a, b: 6)  # always an O-piece

    def open_(name):
        manager = SceneManager("errorScene", screen)
        EventManager.changeScene("errorScene", name)
        return manager

    return open_


def current_game(manager):
    return manager.CURRENT_SCENE.game


def test_key_presses_flow_through_to_the_game(open_scene, send_keys):
    manager = open_scene("endlessTestScene")
    send_keys(pygame.K_RIGHT, pygame.K_RIGHT, pygame.K_SPACE)
    manager.update()

    # O-piece moved two columns right, then locked on the floor
    board = current_game(manager).board
    assert is_filled(board, 19, 6) and is_filled(board, 19, 7)


def test_filling_the_bottom_rows_clears_them_and_scores(open_scene, send_keys):
    manager = open_scene("endlessTestScene")
    for shift in (-4, -2, 0, 2, 4):  # five O-pieces side by side
        key = pygame.K_RIGHT if shift > 0 else pygame.K_LEFT
        send_keys(*[key] * abs(shift), pygame.K_SPACE)
        manager.update()

    game = current_game(manager)
    assert game.score == 4  # two lines -> 2**2
    assert all(game.board.is_row_empty(row) for row in range(game.height))


def test_mission_piece_lands_on_the_mission_stack(open_scene, send_keys):
    manager = open_scene("missionTestScene")
    send_keys(pygame.K_SPACE)
    manager.update()

    board = current_game(manager).board
    # column 4's highest mission block is row 13, so the O rests on rows 11-12
    assert is_filled(board, 12, 4) and is_filled(board, 11, 4)
    assert not is_filled(board, 10, 4)


def test_start_button_scene_restarts_into_endless_with_r(open_scene, send_keys):
    manager = open_scene("testScene")
    assert current_game(manager).state == "gameover"
    send_keys(pygame.K_r)
    manager.update()
    game = current_game(manager)
    assert game.state == "start" and game.is_mission is False


def test_mission_restart_uses_the_board_picked_on_game_over(open_scene, send_keys):
    manager = open_scene("missionTestScene")
    game = current_game(manager)
    game.state = "gameover"

    send_keys(pygame.K_RIGHT, pygame.K_r)
    manager.update()

    assert game.state == "start"
    assert game.is_mission is True
    assert game.mission_board == 1


def test_mission_game_ends_when_the_goal_row_is_cleared(open_scene, send_keys):
    manager = open_scene("missionTestScene")
    game = current_game(manager)
    for cell in game.board.grid[MISSION_GOAL_ROW]:
        cell.clear()
    send_keys(pygame.K_SPACE)
    manager.update()
    assert game.state == "gameover"


def test_m_on_game_over_returns_to_the_main_menu(open_scene, send_keys, monkeypatch):
    # StartScene loads its button images from src/assets, relative to the repo
    monkeypatch.chdir(REPO_ROOT)
    pygame.display.set_mode((1, 1))
    manager = open_scene("endlessTestScene")
    current_game(manager).state = "gameover"

    send_keys(pygame.K_m)
    manager.update()

    assert manager.CURRENT_SCENE is manager.SCENES["startScene"]
