"""
Acceptance: player stories, played one key press per frame through the
real game scene with gravity on. Every piece is an O-piece so each
story plays out the same way.
"""

import random

import pygame
import pytest

from elements.missionData.mission_data import MISSION_FIELD
# aliased so pytest doesn't try to collect it as a test class
from elements.scenes.testScene import TestScene as GameScene


@pytest.fixture
def play(screen, send_keys, monkeypatch):
    monkeypatch.setattr(random, "randint", lambda a, b: 6)
    scene = GameScene(screen)
    scene.enter()

    def press(*keys):
        for key in keys:
            send_keys(key)
            scene.update()
        return scene.game

    return press


def fill_bottom_two_rows(play):
    for shift in (-4, -2, 0, 2, 4):
        key = pygame.K_RIGHT if shift > 0 else pygame.K_LEFT
        play(*[key] * abs(shift), pygame.K_SPACE)


def test_player_opens_the_game_and_picks_a_mode(play):
    game = play()
    assert game.state == "gameover"  # mode-select screen

    game = play(pygame.K_m)
    assert game.state == "start"
    assert game.board.grid == MISSION_FIELD


def test_player_clears_two_lines_and_scores_four(play):
    play(pygame.K_s)
    fill_bottom_two_rows(play)
    assert play().score == 4


def test_player_loses_then_restarts_keeping_their_high_score(play):
    play(pygame.K_s)
    fill_bottom_two_rows(play)
    game = play(*[pygame.K_SPACE] * 10)  # stack to the top
    assert game.state == "gameover"

    game = play(pygame.K_s)
    assert (game.score, game.high_score) == (0, 4)


def test_player_quits_from_the_mode_select_screen(play, quit_calls):
    play(pygame.K_q)
    assert quit_calls == ["quit"]
