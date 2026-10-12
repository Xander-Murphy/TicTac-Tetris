"""UIMenu input handling, using a RecordingGame in place of a real Game."""

import pygame
import pytest

from elements.UI.gameUI import UIMenu


class RecordingGame:
    def __init__(self, state):
        self.state = state
        self.calls = []

    def __getattr__(self, name):
        return lambda *args, **kwargs: self.calls.append((name, *args, *kwargs.values()))


@pytest.mark.parametrize("key, expected", [
    (pygame.K_UP, ("rotate_current_piece",)),
    (pygame.K_LEFT, ("move_left",)),
    (pygame.K_RIGHT, ("move_right",)),
    (pygame.K_SPACE, ("hard_drop",)),
])
def test_playing_keys_call_the_matching_game_method(screen, send_keys, key, expected):
    game = RecordingGame("start")
    send_keys(key)
    UIMenu(screen).handle_input(game)
    assert game.calls == [expected]


@pytest.mark.parametrize("key, is_mission", [(pygame.K_s, False), (pygame.K_m, True)])
def test_mode_keys_start_a_new_game(screen, send_keys, key, is_mission):
    game = RecordingGame("gameover")
    send_keys(key)
    UIMenu(screen).handle_input(game)
    assert game.calls == [("reset", 20, 10, is_mission)]


def test_down_key_is_tracked_until_released(screen, send_keys, monkeypatch):
    ui, game = UIMenu(screen), RecordingGame("start")
    send_keys(pygame.K_DOWN)
    ui.handle_input(game)
    assert ui.pressing_down is True

    release = pygame.event.Event(pygame.KEYUP, key=pygame.K_DOWN)
    monkeypatch.setattr(pygame.event, "get", lambda *a: [release])
    ui.handle_input(game)
    assert ui.pressing_down is False


def test_q_on_the_game_over_screen_quits(screen, send_keys, quit_calls):
    send_keys(pygame.K_q)
    UIMenu(screen).handle_input(RecordingGame("gameover"))
    assert quit_calls == ["quit"]
