"""
StartScene and TestScene update() logic. enter() loads images and builds
a Game/UIMenu, so these tests set fakes on the scene instead.
"""

from types import SimpleNamespace

import pytest

from elements.scenes.startScene import StartScene
# aliased so pytest doesn't try to collect it as a test class
from elements.scenes.testScene import TestScene as GameScene


def button(clicked):
    return SimpleNamespace(is_clicked=lambda: clicked)


@pytest.mark.parametrize("start, quit, expected_events, expected_quits", [
    (True, False, ["testScene"], []),
    (False, True, [], ["quit"]),
])
def test_start_scene_buttons(screen, quit_calls, start, quit, expected_events, expected_quits):
    scene = StartScene(screen)
    scene.imageButtons = {"Start Button": button(start), "Quit Button": button(quit)}
    scene.update()
    assert [event[2] for event in scene.EVENTS] == expected_events
    assert quit_calls == expected_quits


class FakeUI:
    def __init__(self):
        self.pressing_down = False
        self.drawn = []

    def handle_input(self, game):
        pass

    def __getattr__(self, name):  # draw_board, draw_piece, draw_hud, ...
        return lambda *args: self.drawn.append(name)


def game_scene(screen, state):
    scene = GameScene(screen)
    scene.counter, scene.FPS = 0, 25
    scene.game = SimpleNamespace(state=state, board=None, current_piece=None,
                                 score=0, high_score=0, drops=0)
    scene.game.soft_drop = lambda: setattr(scene.game, "drops", scene.game.drops + 1)
    scene.ui = FakeUI()
    return scene


def test_gravity_drops_the_piece_every_half_second(screen):
    scene = game_scene(screen, "start")
    for _ in range(36):  # 36 frames at 25 FPS, a drop every 12
        scene.update()
    assert scene.game.drops == 3


def test_game_over_screen_has_no_gravity_and_no_board(screen):
    scene = game_scene(screen, "gameover")
    scene.ui.pressing_down = True
    for _ in range(12):
        scene.update()
    assert scene.game.drops == 0
    assert "draw_board" not in scene.ui.drawn
    assert "draw_game_over_screen" in scene.ui.drawn
