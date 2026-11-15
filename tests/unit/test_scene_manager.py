"""
SceneManager's real scenes load images and build a Game when entered,
so they're swapped for RecordingScene, which only logs its lifecycle calls.
"""

import pytest

import elements.sceneManager as scene_manager_module
from elements.eventManager import EventManager
from elements.sceneManager import SceneManager
from elements.scenes.scene import Scene


class RecordingScene(Scene):
    def __init__(self, screen, name="default"):
        super().__init__(screen, name)
        self.calls = []

    def enter(self):
        self.calls.append("enter")

    def update(self):
        self.calls.append("update")

    def exit(self):
        self.calls.append("exit")


@pytest.fixture
def manager(monkeypatch, screen):
    for class_name in ("TestScene", "ErrorScene", "StartScene",
                       "MissionTestScene", "EndlessTestScene"):
        monkeypatch.setattr(scene_manager_module, class_name, RecordingScene)
    return SceneManager("startScene", screen)


def test_unknown_initial_scene_raises(manager, screen):
    with pytest.raises(KeyError):
        SceneManager("noSuchScene", screen)


def test_change_scene_exits_old_and_enters_new(manager):
    start, game = manager.SCENES["startScene"], manager.SCENES["testScene"]
    manager.change_scene(start, "testScene")
    assert manager.CURRENT_SCENE is game
    assert start.calls == ["enter", "exit"]
    assert game.calls == ["enter"]


@pytest.mark.parametrize("from_scene, to_scene", [
    ("startScene", "noSuchScene"),  # unknown target
    ("errorScene", "testScene"),    # not the current scene
])
def test_invalid_change_scene_raises_and_stays_put(manager, from_scene, to_scene):
    start = manager.CURRENT_SCENE
    with pytest.raises(KeyError):
        manager.change_scene(manager.SCENES[from_scene], to_scene)
    assert manager.CURRENT_SCENE is start


def test_every_scene_is_registered_by_name(manager):
    assert set(manager.SCENES) == {
        "testScene", "errorScene", "startScene", "missionTestScene", "endlessTestScene",
    }


def test_change_scene_accepts_the_current_scene_by_name(manager):
    manager.change_scene("startScene", "missionTestScene")
    assert manager.CURRENT_SCENE is manager.SCENES["missionTestScene"]


def test_change_scene_by_name_raises_if_that_is_not_the_current_scene(manager):
    start = manager.CURRENT_SCENE
    with pytest.raises(KeyError):
        manager.change_scene("testScene", "endlessTestScene")
    assert manager.CURRENT_SCENE is start


def test_change_scene_rejects_anything_but_a_scene_or_name(manager):
    with pytest.raises(KeyError):
        manager.change_scene(42, "testScene")


def test_event_manager_change_scene_reaches_the_scene_manager(manager):
    EventManager.changeScene("startScene", "endlessTestScene")
    assert manager.CURRENT_SCENE is manager.SCENES["endlessTestScene"]


def test_update_only_updates_the_current_scene(manager):
    manager.update()
    assert manager.SCENES["startScene"].calls == ["enter", "update"]
    assert manager.SCENES["testScene"].calls == []
