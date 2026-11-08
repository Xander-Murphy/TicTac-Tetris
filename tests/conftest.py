"""Shared setup: put src/ on the import path and run pygame headless."""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pygame  # noqa: E402
import pytest  # noqa: E402


@pytest.fixture
def screen():
    pygame.font.init()  # UIMenu builds a font in its constructor
    return pygame.Surface((850, 500))


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
    monkeypatch.setattr(EventManager, "onQuitGame", [lambda: calls.append("quit")])
    return calls
