"""
StartScene and the three game scenes' update() logic. StartScene.enter()
loads images, so the start-screen tests set fake buttons on the scene
instead. The game-scene tests swap in a fake Game and UI.
"""

from types import SimpleNamespace

import pytest

from elements.missionData.mission_data import MISSION_GOAL_ROW
from elements.scenes.endlessTestScene import EndlessTestScene
from elements.scenes.missionTestScene import MissionTestScene
from elements.scenes.startScene import StartScene
# aliased so pytest doesn't try to collect it as a test class
from elements.scenes.testScene import TestScene as GameScene

GAME_SCENES = [GameScene, MissionTestScene, EndlessTestScene]
BUTTONS = ("Start Button", "Quit Button", "Mission Button", "Challenge Button")


# ---------------------------------------------------------------------
# start screen
# ---------------------------------------------------------------------

def button(clicked):
    return SimpleNamespace(is_clicked=lambda: clicked, display=lambda: None)


def start_scene_with(screen, clicked=None):
    scene = StartScene(screen)
    scene.imageButtons = {name: button(name == clicked) for name in BUTTONS}
    return scene


@pytest.mark.parametrize("clicked, next_scene", [
    ("Start Button", "testScene"),
    ("Mission Button", "missionTestScene"),
    ("Challenge Button", "endlessTestScene"),
])
def test_start_scene_buttons_change_scene(screen, scene_changes, quit_calls, clicked, next_scene):
    scene = start_scene_with(screen, clicked)
    scene.update()
    assert scene_changes == [(scene, next_scene)]
    assert quit_calls == []


def test_start_scene_quit_button_quits(screen, scene_changes, quit_calls):
    start_scene_with(screen, "Quit Button").update()
    assert quit_calls == ["quit"]
    assert scene_changes == []


def test_start_scene_does_nothing_without_a_click(screen, scene_changes, quit_calls):
    start_scene_with(screen).update()
    assert scene_changes == [] and quit_calls == []


# ---------------------------------------------------------------------
# game scenes (gravity and drawing)
# ---------------------------------------------------------------------

class FakeUI:
    def __init__(self):
        self.pressing_down = False
        self.drawn = []
        self.input_scene = None

    def handle_input(self, game, scene):
        self.input_scene = scene

    def __getattr__(self, name):  # update_UI, draw_game_over_screen, ...
        return lambda *args: self.drawn.append((name, *args))


def game_scene(screen, scene_class, state, is_mission=False):
    scene = scene_class(screen, "someScene")
    scene.counter, scene.FPS = 0, 25
    scene.game = SimpleNamespace(state=state, board=None, current_piece=None,
                                 score=0, high_score=0, drops=0, is_mission=is_mission,
                                 goal_row=MISSION_GOAL_ROW if is_mission else None)
    scene.game.soft_drop = lambda: setattr(scene.game, "drops", scene.game.drops + 1)
    scene.ui = FakeUI()
    return scene


def drawn_names(scene):
    return [call[0] for call in scene.ui.drawn]


@pytest.mark.parametrize("scene_class", GAME_SCENES)
def test_gravity_drops_the_piece_every_half_second(screen, scene_class):
    scene = game_scene(screen, scene_class, "start")
    for _ in range(36):  # 36 frames at 25 FPS, a drop every 12
        scene.update()
    assert scene.game.drops == 3


@pytest.mark.parametrize("scene_class", GAME_SCENES)
def test_holding_down_drops_every_frame(screen, scene_class):
    scene = game_scene(screen, scene_class, "start")
    scene.ui.pressing_down = True
    for _ in range(5):
        scene.update()
    assert scene.game.drops == 5


@pytest.mark.parametrize("scene_class", GAME_SCENES)
def test_game_over_screen_has_no_gravity_and_no_board(screen, scene_class):
    scene = game_scene(screen, scene_class, "gameover")
    scene.ui.pressing_down = True
    for _ in range(12):
        scene.update()
    assert scene.game.drops == 0
    assert "update_UI" not in drawn_names(scene)
    assert "draw_game_over_screen" in drawn_names(scene)


@pytest.mark.parametrize("scene_class", GAME_SCENES)
def test_scene_passes_its_own_name_for_input(screen, scene_class):
    """GameUI needs the scene name so M can go back to the menu from it."""
    scene = game_scene(screen, scene_class, "start")
    scene.update()
    assert scene.ui.input_scene == "someScene"


@pytest.mark.parametrize("scene_class", GAME_SCENES)
@pytest.mark.parametrize("is_mission, goal_row", [(True, MISSION_GOAL_ROW), (False, None)])
def test_scene_passes_the_goal_row_to_the_ui(screen, scene_class, is_mission, goal_row):
    scene = game_scene(screen, scene_class, "start", is_mission)
    scene.update()
    update_call = next(call for call in scene.ui.drawn if call[0] == "update_UI")
    assert update_call[-1] == goal_row


@pytest.mark.parametrize("scene_class", GAME_SCENES)
@pytest.mark.parametrize("is_mission", [True, False])
def test_game_over_screen_knows_the_mode(screen, scene_class, is_mission):
    scene = game_scene(screen, scene_class, "gameover", is_mission)
    scene.update()
    assert ("draw_game_over_screen", is_mission) in scene.ui.drawn


# ---------------------------------------------------------------------
# entering each game scene
# ---------------------------------------------------------------------

def test_start_button_scene_opens_on_the_game_over_screen(screen):
    scene = GameScene(screen, "testScene")
    scene.enter()
    assert scene.game.state == "gameover"


@pytest.mark.parametrize("scene_class, is_mission", [
    (MissionTestScene, True),
    (EndlessTestScene, False),
])
def test_mode_scenes_start_playing_right_away_in_their_mode(screen, scene_class, is_mission):
    scene = scene_class(screen, "someScene")
    scene.enter()
    assert scene.game.state == "start"
    assert scene.game.is_mission is is_mission
