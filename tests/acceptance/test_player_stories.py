"""
Acceptance: player stories, played one key press per frame through the
real game scenes with gravity on. Every piece is an O-piece so each
story plays out the same way.
"""

import random

import pygame
import pytest

from elements.missionData.mission_data import HARD_MISSION_FIELD, MISSION_FIELD
from elements.scenes.endlessTestScene import EndlessTestScene
from elements.scenes.missionTestScene import MissionTestScene
# aliased so pytest doesn't try to collect it as a test class
from elements.scenes.testScene import TestScene as GameScene
from grid_helpers import grid_values


@pytest.fixture
def open_scene(screen, send_keys, monkeypatch):
    """open_scene(SceneClass) -> play(*keys), one key per frame."""
    monkeypatch.setattr(random, "randint", lambda a, b: 6)

    def open_(scene_class):
        scene = scene_class(screen, "someScene")
        scene.enter()

        def play(*keys):
            for key in keys:
                send_keys(key)
                scene.update()
            return scene.game

        return play

    return open_


def fill_bottom_two_rows(play):
    for shift in (-4, -2, 0, 2, 4):
        key = pygame.K_RIGHT if shift > 0 else pygame.K_LEFT
        play(*[key] * abs(shift), pygame.K_SPACE)


def test_player_presses_start_and_r_to_begin_endless(open_scene):
    play = open_scene(GameScene)
    game = play()
    assert game.state == "gameover"  # waiting on the restart prompt

    game = play(pygame.K_r)
    assert game.state == "start"
    assert game.is_mission is False


def test_player_picks_mission_mode_and_gets_the_mission_board(open_scene):
    game = open_scene(MissionTestScene)()
    assert game.state == "start"
    assert grid_values(game.board) == MISSION_FIELD


def test_player_clears_two_lines_and_scores_four(open_scene):
    play = open_scene(EndlessTestScene)
    fill_bottom_two_rows(play)
    assert play().score == 4


def test_player_loses_then_restarts_keeping_their_high_score(open_scene):
    play = open_scene(EndlessTestScene)
    fill_bottom_two_rows(play)
    game = play(*[pygame.K_SPACE] * 10)  # stack to the top
    assert game.state == "gameover"

    game = play(pygame.K_r)
    assert (game.state, game.score, game.high_score) == ("start", 0, 4)


def test_player_finishes_a_mission_then_tries_the_hard_board(open_scene):
    play = open_scene(MissionTestScene)
    game = play()
    game.state = "gameover"  # skip straight to the end of the mission

    game = play(pygame.K_RIGHT, pygame.K_r)
    assert game.state == "start"
    assert grid_values(game.board) == HARD_MISSION_FIELD


def test_player_quits_from_the_game_over_screen(open_scene, quit_calls):
    play = open_scene(GameScene)
    play(pygame.K_q)
    assert quit_calls == ["quit"]
