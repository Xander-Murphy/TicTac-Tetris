"""
Integration: the real SceneManager, TestScene, UIMenu, Game, Board and
Piece working together. Only key presses and the screen are faked.
"""

import random

import pygame
import pytest

from elements.sceneManager import SceneManager


@pytest.fixture
def game_scene(screen, monkeypatch):
    monkeypatch.setattr(random, "randint", lambda a, b: 6)  # always an O-piece
    manager = SceneManager("errorScene", screen)
    manager.change_scene(manager.CURRENT_SCENE, "testScene")
    return manager


def test_key_presses_flow_through_to_the_game(game_scene, send_keys):
    send_keys(pygame.K_s)
    game_scene.update()
    game = game_scene.CURRENT_SCENE.game
    assert game.state == "start"

    send_keys(pygame.K_RIGHT, pygame.K_RIGHT, pygame.K_SPACE)
    game_scene.update()

    # O-piece moved two columns right, then locked on the floor
    assert game.board.grid[19][6] != 0 and game.board.grid[19][7] != 0


def test_filling_the_bottom_rows_clears_them_and_scores(game_scene, send_keys):
    send_keys(pygame.K_s)
    game_scene.update()
    game = game_scene.CURRENT_SCENE.game

    for shift in (-4, -2, 0, 2, 4):  # five O-pieces side by side
        key = pygame.K_RIGHT if shift > 0 else pygame.K_LEFT
        send_keys(*[key] * abs(shift), pygame.K_SPACE)
        game_scene.update()

    assert game.score == 4  # two lines -> 2**2
    assert all(cell == 0 for row in game.board.grid for cell in row)


def test_mission_piece_lands_on_the_mission_stack(game_scene, send_keys):
    send_keys(pygame.K_m)
    game_scene.update()
    send_keys(pygame.K_SPACE)
    game_scene.update()

    grid = game_scene.CURRENT_SCENE.game.board.grid
    # column 4's highest mission block is row 13, so the O rests on rows 11-12
    assert grid[12][4] != 0 and grid[11][4] != 0 and grid[10][4] == 0
