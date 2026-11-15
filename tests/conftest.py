"""Shared setup: put src/ on the import path and run pygame headless."""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.dirname(__file__))  # for grid_helpers

import pygame  # noqa: E402
import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def isolated_game_state(monkeypatch, tmp_path):
    """
    Keeps tests from leaking into each other or into the repo:
    - EventManager's listener lists are class-level, so every
      SceneManager a test builds would otherwise stay subscribed to
      scene changes for the rest of the run.
    - Game writes score.txt to the working directory on game over, so
      tests run from a temp folder instead of the real repo.
    """
    from elements.eventManager import EventManager

    monkeypatch.setattr(EventManager, "onQuitGame", [])
    monkeypatch.setattr(EventManager, "onSceneChange", [])
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def screen():
    pygame.font.init()  # GameUI builds a font in its constructor
    from elements.config import Config
    return pygame.Surface(Config.SCREEN_SIZE)


@pytest.fixture
def send_keys(monkeypatch):
    """send_keys(K_x, ...) queues key presses for the next frame only."""
    queued = []

    def take(*args, **kwargs):
        events = queued[:]
        queued.clear()
        return events

    monkeypatch.setattr(pygame.event, "get", take)

    def send(*keys):
        queued[:] = [pygame.event.Event(pygame.KEYDOWN, key=key) for key in keys]

    return send


@pytest.fixture
def quit_calls(monkeypatch):
    from elements.eventManager import EventManager

    calls = []
    EventManager.onQuitGame.append(lambda: calls.append("quit"))
    return calls


@pytest.fixture
def scene_changes():
    """Records every EventManager.changeScene(current, next) call."""
    from elements.eventManager import EventManager

    calls = []
    EventManager.onSceneChange.append(lambda current, nxt: calls.append((current, nxt)))
    return calls
